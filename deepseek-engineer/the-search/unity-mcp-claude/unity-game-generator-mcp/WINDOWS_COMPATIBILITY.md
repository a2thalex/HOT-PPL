# Windows Compatibility Guide

## Overview

The Unity Game Generator MCP Server has been updated to work seamlessly on Windows systems. This document outlines the Windows-specific improvements and setup instructions.

## Windows Compatibility Improvements

### 1. **Removed Unix Shebang Line**
- Removed `#!/usr/bin/env node` which was causing issues on Windows
- The server now starts properly using `node index.js` on Windows

### 2. **Enhanced Unity Path Detection**
- **Automatic Unity Detection**: The server now automatically detects Unity installations in common Windows locations:
  - `C:\Program Files\Unity\Hub\Editor\{version}\Editor\Unity.exe`
  - `C:\Program Files (x86)\Unity\Hub\Editor\{version}\Editor\Unity.exe`
  - `%USERPROFILE%\Unity\Hub\Editor\{version}\Editor\Unity.exe`

- **Multiple Version Support**: Checks for common Unity versions:
  - 2023.3.0f1 (latest LTS)
  - 2023.2.20f1
  - 2023.1.20f1
  - 2022.3.40f1
  - 2021.3.40f1

### 3. **Windows File System Validation**
- **Path Length Validation**: Ensures project paths don't exceed Windows' 260-character limit
- **Reserved Name Detection**: Prevents use of Windows reserved filenames (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
- **Invalid Character Detection**: Checks for Windows-invalid characters (< > " | ? *)
- **Drive Letter Support**: Properly handles Windows drive letters (C:, D:, etc.)

### 4. **Improved Error Messages**
- Windows-specific error messages and troubleshooting guidance
- Clear instructions for Unity Hub installation and setup

## Setup Instructions

### Prerequisites
1. **Node.js**: Install Node.js 16+ from [nodejs.org](https://nodejs.org)
2. **Unity Hub**: Install Unity Hub from [unity.com](https://unity.com/download)
3. **Unity Editor**: Install Unity 2022.3 LTS or newer through Unity Hub

### Installation
1. Navigate to the project directory:
   ```cmd
   cd the-search\unity-mcp-claude\unity-game-generator-mcp
   ```

2. Install dependencies:
   ```cmd
   npm install
   ```

3. Test the installation:
   ```cmd
   node test-windows.js
   ```

### Running the MCP Server
```cmd
node index.js
```

## Environment Variables

You can customize the behavior using these environment variables:

- **UNITY_PATH**: Override Unity installation path
  ```cmd
  set UNITY_PATH=C:\Program Files\Unity\Hub\Editor\2023.3.0f1\Editor\Unity.exe
  ```

- **WORKSPACE_PATH**: Set custom workspace for Unity projects
  ```cmd
  set WORKSPACE_PATH=C:\Users\YourName\UnityProjects
  ```

## Troubleshooting

### Unity Not Found Error
If you get "Unity not found" errors:
1. Verify Unity Hub is installed
2. Install Unity Editor through Unity Hub
3. Set the UNITY_PATH environment variable manually
4. Check that Unity.exe exists at the specified path

### Path Too Long Error
If you get path length errors:
1. Use shorter project names
2. Create projects closer to the root directory (e.g., C:\Projects\)
3. Enable long path support in Windows 10/11

### Reserved Filename Error
Avoid these reserved Windows filenames:
- CON, PRN, AUX, NUL
- COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9
- LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, LPT9

## Features

The MCP server provides these tools for Windows users:

### create_unity_game
Creates a complete Unity game project with:
- Cross-platform C# scripts
- Windows-compatible file structure
- Unity project files and scenes
- Genre-specific game mechanics (platformer, shooter, puzzle)
- Optional features (save system, achievements)

### generate_unity_script
Generates individual Unity C# scripts for specific purposes.

## Windows-Specific Next Steps

After creating a Unity project:
1. Open Unity Hub
2. Click "Add project from disk"
3. Navigate to the generated project folder
4. Select the project folder
5. Open the project in Unity Editor
6. Test in Play mode

## Support

For Windows-specific issues:
1. Ensure Unity Hub and Unity Editor are properly installed
2. Check Windows file system permissions
3. Verify Node.js is installed and accessible from command line
4. Use Windows-compatible paths (avoid special characters)
