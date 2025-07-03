# 🐋 DeepSeek Engineer GUI

A modern graphical user interface for the DeepSeek Engineer AI coding assistant.

## Features

### 🎨 **Modern Dark Theme Interface**
- Clean, professional dark theme optimized for coding
- Responsive layout with resizable panels
- Color-coded message types for easy reading

### 🧠 **AI Capabilities**
- **Elite Software Engineering**: Decades of experience across all programming domains
- **Chain of Thought Reasoning**: Visible thought process before providing solutions
- **Real-time Streaming**: See the AI's reasoning and responses as they're generated
- **Function Calling**: Automatic file operations through intelligent function calls

### 📁 **File Operations**
- **Add Files**: Click to add individual files to conversation context
- **Add Folders**: Bulk add entire directories with smart filtering
- **Context Management**: Visual list of files in current context
- **Automatic File Reading**: AI can read files mentioned in conversation
- **File Creation & Editing**: AI can create new files and edit existing ones

### 💬 **Chat Interface**
- **Real-time Streaming**: See responses as they're generated
- **Color-coded Messages**: Different colors for user, assistant, reasoning, and function calls
- **Keyboard Shortcuts**: Ctrl+Enter to send messages
- **Message History**: Full conversation history with scrolling

### 🛠️ **Function Calling Tools**
The AI can automatically execute these operations:
- `read_file` - Read single file content
- `read_multiple_files` - Read multiple files at once  
- `create_file` - Create new files or overwrite existing ones
- `create_multiple_files` - Create multiple files in one operation
- `edit_file` - Make precise edits to existing files

## Installation & Setup

### Prerequisites
1. **Python 3.11+** installed
2. **DeepSeek API Key** from [DeepSeek Platform](https://platform.deepseek.com)
3. **Dependencies** installed (see main README.md)

### Quick Start

1. **Ensure dependencies are installed**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key** in `.env` file:
   ```
   DEEPSEEK_API_KEY=your_api_key_here
   ```

3. **Launch the GUI**:
   ```bash
   # Using Python directly
   python deepseek-gui.py
   
   # Using launcher scripts
   .\launch-gui.bat        # Windows Batch
   .\launch-gui.ps1        # PowerShell
   ```

## How to Use

### 🚀 **Getting Started**
1. Launch the GUI using one of the methods above
2. The interface will open with a welcome message
3. Start by adding files or folders to context (optional)
4. Type your questions or requests in the input box
5. Press Ctrl+Enter or click "Send" to submit

### 📁 **Adding Context**
- **Add File**: Click "📄 Add File" to select individual files
- **Add Folder**: Click "📁 Add Folder" to add entire directories
- **Context List**: View all added files in the left panel
- **Clear Context**: Remove all context with "🗑️ Clear Context"

### 💬 **Chatting with the AI**
- Type naturally - the AI will understand your requests
- Mention files by name and the AI will automatically read them
- Ask for code reviews, bug fixes, new features, etc.
- Use Ctrl+Enter as a keyboard shortcut to send messages

### 🎨 **Message Types**
- **🔵 Blue**: Your messages
- **⚪ White**: AI responses
- **🟡 Yellow**: AI reasoning (Chain of Thought)
- **🟢 Green**: Function calls and success messages
- **🔴 Red**: Error messages

## Example Usage

### Code Review
```
You: Can you review the main.py file and suggest improvements?
```
The AI will automatically read main.py and provide detailed feedback.

### Create New Features
```
You: Create a new authentication module with login and registration functions
```
The AI will create multiple files with complete authentication functionality.

### Debug Issues
```
You: There's a bug in the user registration function, can you fix it?
```
The AI will read the relevant files, identify the issue, and fix it.

### Project Analysis
```
You: Analyze this entire project structure and suggest a refactoring plan
```
Add the project folder to context, then ask for analysis.

## Keyboard Shortcuts

- **Ctrl+Enter**: Send message
- **Escape**: Clear input field (when focused)

## Troubleshooting

### GUI Won't Start
- Ensure Python 3.11+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify your API key is set in the `.env` file

### API Errors
- Check your DeepSeek API key is valid
- Ensure you have sufficient API credits
- Check your internet connection

### File Operation Errors
- Ensure you have write permissions in the working directory
- Check file paths are correct and accessible
- Large files (>5MB) are automatically skipped

## Features Comparison

| Feature | CLI Version | GUI Version |
|---------|-------------|-------------|
| AI Chat | ✅ Terminal | ✅ Rich Interface |
| File Operations | ✅ Commands | ✅ Click & Drag |
| Context Management | ✅ Manual | ✅ Visual List |
| Real-time Streaming | ✅ Text | ✅ Color-coded |
| Function Calls | ✅ Text Output | ✅ Visual Feedback |
| Ease of Use | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## Technical Details

- **Framework**: tkinter with ttk for modern styling
- **Threading**: Background processing to prevent GUI freezing
- **Streaming**: Real-time display of AI responses
- **Security**: Same path validation and file size limits as CLI version
- **Performance**: Optimized for smooth interaction with large codebases

---

**Enjoy coding with your AI assistant! 🚀**
