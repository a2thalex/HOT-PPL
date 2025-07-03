#!/usr/bin/env python3

import os
import sys
import json
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from pathlib import Path
from typing import List, Dict, Any, Optional
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import time

# Load environment and configure OpenAI client
load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# System prompt
system_PROMPT = """You are an elite software engineer called DeepSeek Engineer with decades of experience across all programming domains.
Your expertise spans system design, algorithms, testing, and best practices.
You provide thoughtful, well-structured solutions while explaining your reasoning.

Core capabilities:
1. Code Analysis & Discussion
   - Analyze code with expert-level insight
   - Explain complex concepts clearly
   - Suggest optimizations and best practices
   - Debug issues with precision

2. File Operations (via function calls):
   - read_file: Read a single file's content
   - read_multiple_files: Read multiple files at once
   - create_file: Create or overwrite a single file
   - create_multiple_files: Create multiple files at once
   - edit_file: Make precise edits to existing files using snippet replacement

Guidelines:
1. Provide natural, conversational responses explaining your reasoning
2. Use function calls when you need to read or modify files
3. For file operations:
   - Always read files first before editing them to understand the context
   - Use precise snippet matching for edits
   - Explain what changes you're making and why
   - Consider the impact of changes on the overall codebase
4. Follow language-specific best practices
5. Suggest tests or validation steps when appropriate
6. Be thorough in your analysis and recommendations

IMPORTANT: In your thinking process, if you realize that something requires a tool call, cut your thinking short and proceed directly to the tool call. Don't overthink - act efficiently when file operations are needed.

Remember: You're a senior engineer - be thoughtful, precise, and explain your reasoning clearly."""

# Function calling tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the content of a single file from the filesystem",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read (relative or absolute)",
                    }
                },
                "required": ["file_path"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_multiple_files",
            "description": "Read the content of multiple files from the filesystem",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of file paths to read (relative or absolute)",
                    }
                },
                "required": ["file_paths"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Create a new file or overwrite an existing file with the provided content",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path where the file should be created",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file",
                    }
                },
                "required": ["file_path", "content"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_multiple_files",
            "description": "Create multiple files at once",
            "parameters": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "content": {"type": "string"}
                            },
                            "required": ["path", "content"]
                        },
                        "description": "Array of files to create with their paths and content",
                    }
                },
                "required": ["files"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Edit an existing file by replacing a specific snippet with new content",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to edit",
                    },
                    "original_snippet": {
                        "type": "string",
                        "description": "The exact text snippet to find and replace",
                    },
                    "new_snippet": {
                        "type": "string",
                        "description": "The new text to replace the original snippet with",
                    }
                },
                "required": ["file_path", "original_snippet", "new_snippet"]
            },
        }
    }
]

# Conversation history
conversation_history = [
    {"role": "system", "content": system_PROMPT}
]

# Utility functions
def normalize_path(path_str: str) -> str:
    """Return a canonical, absolute version of the path with security checks."""
    path = Path(path_str).resolve()

    # Prevent directory traversal attacks
    if ".." in path.parts:
        raise ValueError(f"Invalid path: {path_str} contains parent directory references")

    return str(path)

def read_local_file(file_path: str) -> str:
    """Return the text content of a local file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def create_file(path: str, content: str):
    """Create (or overwrite) a file at 'path' with the given 'content'."""
    file_path = Path(path)

    # Security checks
    if any(part.startswith('~') for part in file_path.parts):
        raise ValueError("Home directory references not allowed")
    normalized_path = normalize_path(str(file_path))

    # Validate reasonable file size for operations
    if len(content) > 5_000_000:  # 5MB limit
        raise ValueError("File content exceeds 5MB size limit")

    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def is_binary_file(file_path: str, peek_size: int = 1024) -> bool:
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(peek_size)
        # If there is a null byte in the sample, treat it as binary
        if b'\0' in chunk:
            return True
        return False
    except Exception:
        # If we fail to read, just treat it as binary to be safe
        return True

def try_handle_add_command(user_input: str) -> bool:
    prefix = "/add "
    if user_input.strip().lower().startswith(prefix):
        path_to_add = user_input[len(prefix):].strip()
        try:
            normalized_path = normalize_path(path_to_add)
            if os.path.isdir(normalized_path):
                # Handle entire directory
                add_directory_to_conversation(normalized_path)
            else:
                # Handle a single file as before
                content = read_local_file(normalized_path)
                conversation_history.append({
                    "role": "system",
                    "content": f"Content of file '{normalized_path}':\n\n{content}"
                })
        except OSError as e:
            print(f"Could not add path '{path_to_add}': {e}")
        return True
    return False

def add_directory_to_conversation(directory_path: str):
    excluded_files = {
        # Python specific
        ".DS_Store", "Thumbs.db", ".gitignore", ".python-version",
        "uv.lock", ".uv", "uvenv", ".uvenv", ".venv", "venv",
        "__pycache__", ".pytest_cache", ".coverage", ".mypy_cache",
        # Node.js / Web specific
        "node_modules", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
        ".next", ".nuxt", "dist", "build", ".cache", ".parcel-cache",
        ".turbo", ".vercel", ".output", ".contentlayer",
        # Build outputs
        "out", "coverage", ".nyc_output", "storybook-static",
        # Environment and config
        ".env", ".env.local", ".env.development", ".env.production",
        # Misc
        ".git", ".svn", ".hg", "CVS"
    }
    excluded_extensions = {
        # Binary and media files
        ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".avif",
        ".mp4", ".webm", ".mov", ".mp3", ".wav", ".ogg",
        ".zip", ".tar", ".gz", ".7z", ".rar",
        ".exe", ".dll", ".so", ".dylib", ".bin",
        # Documents
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        # Python specific
        ".pyc", ".pyo", ".pyd", ".egg", ".whl",
        # UV specific
        ".uv", ".uvenv",
        # Database and logs
        ".db", ".sqlite", ".sqlite3", ".log",
        # IDE specific
        ".idea", ".vscode",
        # Web specific
        ".map", ".chunk.js", ".chunk.css",
        ".min.js", ".min.css", ".bundle.js", ".bundle.css",
        # Cache and temp files
        ".cache", ".tmp", ".temp",
        # Font files
        ".ttf", ".otf", ".woff", ".woff2", ".eot"
    }

    added_files = []
    total_files_processed = 0
    max_files = 100  # Reasonable limit for files to process
    max_file_size = 5_000_000  # 5MB limit

    for root, dirs, files in os.walk(directory_path):
        if total_files_processed >= max_files:
            break

        # Skip hidden directories and excluded directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in excluded_files]

        for file in files:
            if total_files_processed >= max_files:
                break

            if file.startswith('.') or file in excluded_files:
                continue

            _, ext = os.path.splitext(file)
            if ext.lower() in excluded_extensions:
                continue

            full_path = os.path.join(root, file)

            try:
                # Check file size before processing
                if os.path.getsize(full_path) > max_file_size:
                    continue

                # Check if it's binary
                if is_binary_file(full_path):
                    continue

                normalized_path = normalize_path(full_path)
                content = read_local_file(normalized_path)
                conversation_history.append({
                    "role": "system",
                    "content": f"Content of file '{normalized_path}':\n\n{content}"
                })
                added_files.append(normalized_path)
                total_files_processed += 1

            except OSError:
                continue

def execute_function_call_dict(tool_call_dict) -> str:
    """Execute a function call from a dictionary format and return the result as a string."""
    try:
        function_name = tool_call_dict["function"]["name"]
        arguments = json.loads(tool_call_dict["function"]["arguments"])

        if function_name == "read_file":
            file_path = arguments["file_path"]
            normalized_path = normalize_path(file_path)
            content = read_local_file(normalized_path)
            return f"Content of file '{normalized_path}':\n\n{content}"

        elif function_name == "read_multiple_files":
            file_paths = arguments["file_paths"]
            results = []
            for file_path in file_paths:
                try:
                    normalized_path = normalize_path(file_path)
                    content = read_local_file(normalized_path)
                    results.append(f"Content of file '{normalized_path}':\n\n{content}")
                except OSError as e:
                    results.append(f"Error reading '{file_path}': {e}")
            return "\n\n" + "="*50 + "\n\n".join(results)

        elif function_name == "create_file":
            file_path = arguments["file_path"]
            content = arguments["content"]
            create_file(file_path, content)
            return f"Successfully created file '{file_path}'"

        elif function_name == "create_multiple_files":
            files = arguments["files"]
            created_files = []
            for file_info in files:
                create_file(file_info["path"], file_info["content"])
                created_files.append(file_info["path"])
            return f"Successfully created {len(created_files)} files: {', '.join(created_files)}"

        elif function_name == "edit_file":
            file_path = arguments["file_path"]
            original_snippet = arguments["original_snippet"]
            new_snippet = arguments["new_snippet"]

            # Read file and apply edit
            content = read_local_file(file_path)
            if original_snippet not in content:
                return f"Error: Original snippet not found in '{file_path}'"

            updated_content = content.replace(original_snippet, new_snippet, 1)
            create_file(file_path, updated_content)
            return f"Successfully edited file '{file_path}'"

        else:
            return f"Unknown function: {function_name}"

    except Exception as e:
        return f"Error executing {function_name}: {str(e)}"

class DeepSeekGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐋 DeepSeek Engineer GUI")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Configure style
        self.setup_styles()
        
        # Create main layout
        self.create_widgets()
        
        # Initialize conversation
        self.conversation_active = False
        
    def setup_styles(self):
        """Configure ttk styles for dark theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure('TFrame', background='#1e1e1e')
        style.configure('TLabel', background='#1e1e1e', foreground='#ffffff')
        style.configure('TButton', background='#0066ff', foreground='#ffffff')
        style.map('TButton', background=[('active', '#3b82f6')])
        style.configure('TEntry', background='#2d2d2d', foreground='#ffffff')
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Left panel - File operations
        self.create_left_panel(content_frame)
        
        # Right panel - Chat interface
        self.create_right_panel(content_frame)
        
        # Bottom panel - Input area
        self.create_bottom_panel(main_frame)
        
    def create_header(self, parent):
        """Create the header with title and status"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text="🐋 DeepSeek Engineer with Function Calling",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(side=tk.LEFT)
        
        # Status indicator
        self.status_label = ttk.Label(
            header_frame,
            text="● Ready",
            font=('Arial', 10),
            foreground='#00ff00'
        )
        self.status_label.pack(side=tk.RIGHT)
        
    def create_left_panel(self, parent):
        """Create the left panel for file operations"""
        left_frame = ttk.Frame(parent)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # File operations section
        file_label = ttk.Label(left_frame, text="📁 File Operations", font=('Arial', 12, 'bold'))
        file_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Add file button
        add_file_btn = ttk.Button(
            left_frame,
            text="📄 Add File",
            command=self.add_file,
            width=20
        )
        add_file_btn.pack(fill=tk.X, pady=2)
        
        # Add folder button
        add_folder_btn = ttk.Button(
            left_frame,
            text="📁 Add Folder",
            command=self.add_folder,
            width=20
        )
        add_folder_btn.pack(fill=tk.X, pady=2)
        
        # Context files list
        context_label = ttk.Label(left_frame, text="Context Files:", font=('Arial', 10, 'bold'))
        context_label.pack(anchor=tk.W, pady=(20, 5))
        
        # Context listbox with scrollbar
        context_frame = ttk.Frame(left_frame)
        context_frame.pack(fill=tk.BOTH, expand=True)
        
        self.context_listbox = tk.Listbox(
            context_frame,
            bg='#2d2d2d',
            fg='#ffffff',
            selectbackground='#0066ff',
            font=('Consolas', 9)
        )
        context_scrollbar = ttk.Scrollbar(context_frame, orient=tk.VERTICAL)
        
        self.context_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        context_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.context_listbox.config(yscrollcommand=context_scrollbar.set)
        context_scrollbar.config(command=self.context_listbox.yview)
        
        # Clear context button
        clear_btn = ttk.Button(
            left_frame,
            text="🗑️ Clear Context",
            command=self.clear_context,
            width=20
        )
        clear_btn.pack(fill=tk.X, pady=(10, 0))
        
    def create_right_panel(self, parent):
        """Create the right panel for chat interface"""
        right_frame = ttk.Frame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat history
        chat_label = ttk.Label(right_frame, text="💬 Conversation", font=('Arial', 12, 'bold'))
        chat_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            right_frame,
            bg='#1e1e1e',
            fg='#ffffff',
            font=('Consolas', 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for different message types
        self.setup_chat_tags()
        
    def create_bottom_panel(self, parent):
        """Create the bottom panel for input"""
        bottom_frame = ttk.Frame(parent)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Input area
        input_frame = ttk.Frame(bottom_frame)
        input_frame.pack(fill=tk.X)
        
        # Input text box
        self.input_text = tk.Text(
            input_frame,
            height=3,
            bg='#2d2d2d',
            fg='#ffffff',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="🚀 Send",
            command=self.send_message,
            width=10
        )
        self.send_button.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind Enter key to send message
        self.input_text.bind('<Control-Return>', lambda event: self.send_message())
        
    def setup_chat_tags(self):
        """Setup text tags for different message types"""
        self.chat_display.tag_configure('user', foreground='#00aaff', font=('Consolas', 10, 'bold'))
        self.chat_display.tag_configure('assistant', foreground='#ffffff')
        self.chat_display.tag_configure('reasoning', foreground='#ffaa00', font=('Consolas', 9, 'italic'))
        self.chat_display.tag_configure('function', foreground='#00ff88', font=('Consolas', 9))
        self.chat_display.tag_configure('error', foreground='#ff4444', font=('Consolas', 10, 'bold'))
        self.chat_display.tag_configure('success', foreground='#44ff44', font=('Consolas', 10, 'bold'))
        
    def add_to_chat(self, message: str, tag: str = 'assistant'):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + '\n\n', tag)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def update_status(self, status: str, color: str = '#00ff00'):
        """Update the status indicator"""
        self.status_label.config(text=f"● {status}", foreground=color)
        
    def add_file(self):
        """Add a single file to context"""
        file_path = filedialog.askopenfilename(
            title="Select file to add to context",
            filetypes=[("All files", "*.*"), ("Python files", "*.py"), ("Text files", "*.txt")]
        )
        
        if file_path:
            try:
                normalized_path = normalize_path(file_path)
                content = read_local_file(normalized_path)
                conversation_history.append({
                    "role": "system",
                    "content": f"Content of file '{normalized_path}':\n\n{content}"
                })
                
                # Add to context list
                self.context_listbox.insert(tk.END, os.path.basename(file_path))
                self.add_to_chat(f"✓ Added file '{os.path.basename(file_path)}' to context", 'success')
                
            except Exception as e:
                self.add_to_chat(f"✗ Error adding file: {str(e)}", 'error')
                
    def add_folder(self):
        """Add a folder to context"""
        folder_path = filedialog.askdirectory(title="Select folder to add to context")
        
        if folder_path:
            try:
                self.update_status("Adding folder...", '#ffaa00')
                # Run in thread to prevent GUI freezing
                threading.Thread(
                    target=self._add_folder_thread,
                    args=(folder_path,),
                    daemon=True
                ).start()
                
            except Exception as e:
                self.add_to_chat(f"✗ Error adding folder: {str(e)}", 'error')
                self.update_status("Ready")
                
    def _add_folder_thread(self, folder_path):
        """Add folder in background thread"""
        try:
            # Use the existing function from the original script
            add_directory_to_conversation(folder_path)
            
            # Update GUI in main thread
            self.root.after(0, lambda: self._folder_added_callback(folder_path))
            
        except Exception as e:
            self.root.after(0, lambda: self.add_to_chat(f"✗ Error adding folder: {str(e)}", 'error'))
            self.root.after(0, lambda: self.update_status("Ready"))
            
    def _folder_added_callback(self, folder_path):
        """Callback when folder is successfully added"""
        self.context_listbox.insert(tk.END, f"📁 {os.path.basename(folder_path)}")
        self.add_to_chat(f"✓ Added folder '{os.path.basename(folder_path)}' to context", 'success')
        self.update_status("Ready")
        
    def clear_context(self):
        """Clear the conversation context"""
        global conversation_history
        conversation_history = [{"role": "system", "content": system_PROMPT}]
        self.context_listbox.delete(0, tk.END)
        self.add_to_chat("🗑️ Context cleared", 'function')
        
    def send_message(self):
        """Send a message to the AI"""
        message = self.input_text.get(1.0, tk.END).strip()
        
        if not message:
            return
            
        # Clear input
        self.input_text.delete(1.0, tk.END)
        
        # Add user message to chat
        self.add_to_chat(f"🔵 You: {message}", 'user')
        
        # Check for /add command
        if try_handle_add_command(message):
            return
            
        # Disable send button and update status
        self.send_button.config(state=tk.DISABLED)
        self.update_status("Thinking...", '#ffaa00')
        
        # Process message in background thread
        threading.Thread(
            target=self._process_message_thread,
            args=(message,),
            daemon=True
        ).start()
        
    def _process_message_thread(self, message):
        """Process AI message in background thread"""
        try:
            # Use the existing streaming function
            response_data = self.stream_openai_response_gui(message)
            
            # Re-enable send button in main thread
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.update_status("Ready"))
            
            if response_data.get("error"):
                self.root.after(0, lambda: self.add_to_chat(f"❌ Error: {response_data['error']}", 'error'))
                
        except Exception as e:
            self.root.after(0, lambda: self.add_to_chat(f"❌ Unexpected error: {str(e)}", 'error'))
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.update_status("Ready"))

    def stream_openai_response_gui(self, user_message: str):
        """Modified version of stream_openai_response for GUI"""
        # Add the user message to conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Trim conversation history if it's getting too long
        self.trim_conversation_history()

        try:
            stream = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=conversation_history,
                tools=tools,
                max_completion_tokens=64000,
                stream=True
            )

            self.root.after(0, lambda: self.add_to_chat("🐋 Seeking...", 'function'))
            reasoning_started = False
            reasoning_content = ""
            final_content = ""
            tool_calls = []

            assistant_message = {
                "role": "assistant",
                "content": "",
                "tool_calls": []
            }

            for chunk in stream:
                if chunk.choices[0].delta.reasoning:
                    if not reasoning_started:
                        reasoning_started = True
                        self.root.after(0, lambda: self.add_to_chat("💭 Reasoning:", 'reasoning'))

                    reasoning_chunk = chunk.choices[0].delta.reasoning
                    reasoning_content += reasoning_chunk
                    # Update reasoning display in real-time
                    self.root.after(0, lambda rc=reasoning_chunk: self._append_to_last_message(rc, 'reasoning'))

                if chunk.choices[0].delta.content:
                    if reasoning_started and not final_content:
                        self.root.after(0, lambda: self.add_to_chat("🤖 Assistant:", 'assistant'))

                    content_chunk = chunk.choices[0].delta.content
                    final_content += content_chunk
                    assistant_message["content"] += content_chunk
                    # Update content display in real-time
                    self.root.after(0, lambda cc=content_chunk: self._append_to_last_message(cc, 'assistant'))

                if chunk.choices[0].delta.tool_calls:
                    for tool_call_delta in chunk.choices[0].delta.tool_calls:
                        # Handle tool call streaming
                        if tool_call_delta.index >= len(tool_calls):
                            tool_calls.append({
                                "id": "",
                                "type": "function",
                                "function": {"name": "", "arguments": ""}
                            })

                        if tool_call_delta.id:
                            tool_calls[tool_call_delta.index]["id"] = tool_call_delta.id
                        if tool_call_delta.function.name:
                            tool_calls[tool_call_delta.index]["function"]["name"] = tool_call_delta.function.name
                        if tool_call_delta.function.arguments:
                            tool_calls[tool_call_delta.index]["function"]["arguments"] += tool_call_delta.function.arguments

            # Handle tool calls if any
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
                conversation_history.append(assistant_message)

                self.root.after(0, lambda: self.add_to_chat(f"⚡ Executing {len(tool_calls)} function call(s)...", 'function'))

                for tool_call in tool_calls:
                    function_name = tool_call["function"]["name"]
                    self.root.after(0, lambda fn=function_name: self.add_to_chat(f"→ {fn}", 'function'))

                    try:
                        result = execute_function_call_dict(tool_call)

                        # Add tool result to conversation immediately
                        tool_response = {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": result
                        }
                        conversation_history.append(tool_response)

                        # Show success message
                        if "Successfully" in result or "Content of file" in result:
                            self.root.after(0, lambda r=result: self.add_to_chat(f"✓ {r.split(':')[0] if ':' in r else r}", 'success'))
                        else:
                            self.root.after(0, lambda r=result: self.add_to_chat(f"ℹ️ {r}", 'function'))

                    except Exception as e:
                        error_msg = f"Error executing {function_name}: {e}"
                        self.root.after(0, lambda em=error_msg: self.add_to_chat(f"✗ {em}", 'error'))
                        # Still need to add a tool response even on error
                        conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": f"Error: {str(e)}"
                        })

                # Get follow-up response after tool execution
                self.root.after(0, lambda: self.add_to_chat("🔄 Processing results...", 'function'))

                follow_up_stream = client.chat.completions.create(
                    model="deepseek-reasoner",
                    messages=conversation_history,
                    tools=tools,
                    max_completion_tokens=64000,
                    stream=True
                )

                follow_up_content = ""
                self.root.after(0, lambda: self.add_to_chat("🤖 Assistant:", 'assistant'))

                for chunk in follow_up_stream:
                    if chunk.choices[0].delta.content:
                        content_chunk = chunk.choices[0].delta.content
                        follow_up_content += content_chunk
                        # Update content display in real-time
                        self.root.after(0, lambda cc=content_chunk: self._append_to_last_message(cc, 'assistant'))

                # Store follow-up response
                conversation_history.append({
                    "role": "assistant",
                    "content": follow_up_content
                })
            else:
                # No tool calls, just store the regular response
                conversation_history.append(assistant_message)

            return {"success": True}

        except Exception as e:
            error_msg = f"DeepSeek API error: {str(e)}"
            return {"error": error_msg}

    def _append_to_last_message(self, text: str, tag: str):
        """Append text to the last message in chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text, tag)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def trim_conversation_history(self):
        """Trim conversation history to prevent token overflow"""
        max_messages = 50  # Keep last 50 messages
        if len(conversation_history) > max_messages:
            # Keep system message and last max_messages-1 messages
            system_msg = conversation_history[0]
            recent_messages = conversation_history[-(max_messages-1):]
            conversation_history.clear()
            conversation_history.append(system_msg)
            conversation_history.extend(recent_messages)


def main():
    """Main function to run the GUI"""
    # Check if API key is configured
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key or api_key == "your_api_key_here":
        messagebox.showerror(
            "API Key Required",
            "Please set your DEEPSEEK_API_KEY in the .env file.\n\n"
            "Get your API key from: https://platform.deepseek.com"
        )
        return

    # Create and run the GUI
    root = tk.Tk()
    app = DeepSeekGUI(root)

    # Add welcome message
    app.add_to_chat(
        "🐋 Welcome to DeepSeek Engineer GUI!\n\n"
        "💡 How to use:\n"
        "• Add files or folders to context using the buttons on the left\n"
        "• Type your questions or requests in the input box below\n"
        "• The AI can automatically read and create files using function calls\n"
        "• Use Ctrl+Enter to send messages\n\n"
        "Ready to help with your coding tasks! 🚀",
        'function'
    )

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nGUI closed by user")


if __name__ == "__main__":
    main()
