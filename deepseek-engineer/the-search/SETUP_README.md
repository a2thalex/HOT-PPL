# HOT PPL: The Search - Development Environment Setup

## Overview

This setup system provides automated installation and configuration of Unity 2023.3 LTS with MCP (Model Context Protocol) integration for autonomous game development. The system follows the specifications outlined in the HOT PPL development plan.

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Double-click setup.bat or run from command line:
setup.bat
```

### Option 2: PowerShell Direct
```powershell
# Run PowerShell as Administrator
.\setup-hotppl-development.ps1 -FullSetup
```

## System Requirements

- **Operating System:** Windows 10/11 (64-bit)
- **PowerShell:** Version 5.0 or higher
- **Disk Space:** 10GB+ free space
- **Memory:** 8GB+ RAM recommended
- **Internet:** Required for downloads
- **Permissions:** Administrator rights recommended

## Setup Components

### 1. Unity 2023.3 LTS Installation
- **Unity Hub:** Latest version
- **Unity Editor:** 2023.3.0f1 with modules:
  - Windows IL2CPP Build Support
  - Universal Windows Platform Build Support
  - WebGL Build Support
  - Android Build Support
  - Documentation
  - Language Pack (English)

### 2. Unity Project Creation
- **Project Name:** HOTPPLTheSearch
- **Template:** 3D (URP)
- **Packages:** Pre-configured with required packages:
  - Input System
  - Cinemachine
  - Timeline
  - Universal Render Pipeline
  - TextMeshPro
  - Netcode for GameObjects
  - ProBuilder
  - Addressables
  - Post Processing

### 3. MCP Server Integration
- **Unity Integration Server:** Project monitoring and automation
- **Task Management Server:** Development coordination
- **Git Integration Server:** Version control automation
- **Performance Monitoring Server:** Real-time performance tracking

## Setup Scripts

### Main Scripts
- **`setup.bat`** - Quick launcher (double-click to run)
- **`setup-hotppl-development.ps1`** - Main orchestration script
- **`setup-unity-cli.ps1`** - Unity installation and project setup
- **`setup-mcp-integration.ps1`** - MCP server configuration

### Configuration Files
- **`mcp-config.json`** - MCP server configuration
- **`package.json`** - Node.js dependencies for MCP servers

## Usage Instructions

### Full Setup (Recommended)
```powershell
.\setup-hotppl-development.ps1 -FullSetup
```
Installs Unity, creates project, configures MCP, and copies character assets.

### Unity Only
```powershell
.\setup-hotppl-development.ps1 -UnityOnly
```
Installs Unity and creates project without MCP integration.

### MCP Only
```powershell
.\setup-hotppl-development.ps1 -MCPOnly
```
Configures MCP integration for existing Unity project.

### Advanced Options
```powershell
# Custom Unity version
.\setup-unity-cli.ps1 -UnityVersion "2023.3.1f1"

# Skip Unity installation (project setup only)
.\setup-unity-cli.ps1 -SkipUnityInstall

# MCP configuration only (no server installation)
.\setup-mcp-integration.ps1 -ConfigureOnly
```

## Post-Setup

### Desktop Shortcuts Created
- **HOT PPL Unity** - Opens Unity project directly
- **HOT PPL Development** - Starts complete development environment

### Development Workflow
1. **Start Development Environment:**
   ```powershell
   .\start-development.ps1
   ```
   This starts all MCP servers and opens Unity.

2. **Unity MCP Integration:**
   - Use `HOTPPL > MCP` menu in Unity
   - Start/stop servers from Unity interface
   - Monitor server status in real-time

3. **Character Asset Setup:**
   ```csharp
   // In Unity, run this in the console or create a script:
   CharacterAssetSetup.SetupCharacterAssets();
   ```

## MCP Server Configuration

### Server Capabilities

#### Unity Integration Server
- Project file monitoring
- Automated build triggers
- Asset validation
- Performance threshold monitoring

#### Task Management Server
- Development phase tracking
- Task dependency management
- Progress reporting
- Milestone monitoring

#### Git Integration Server
- Automated commit coordination
- Branch management
- LFS handling for large assets
- Backup scheduling

#### Performance Monitoring Server
- Real-time FPS monitoring
- Memory usage tracking
- Draw call optimization
- Profiling automation

### Configuration Customization

Edit `mcp-config.json` to customize:
- Performance thresholds
- Monitoring intervals
- Automation rules
- Alert conditions

## Troubleshooting

### Common Issues

#### Unity Installation Fails
- **Solution:** Run as Administrator
- **Check:** Internet connection and firewall settings
- **Alternative:** Install Unity Hub manually from unity.com

#### PowerShell Execution Policy Error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Node.js Not Found
- **Solution:** Run setup with `-InstallMCPServers` flag
- **Manual:** Download from nodejs.org

#### Project Creation Fails
- **Check:** Disk space (10GB+ required)
- **Check:** Unity Hub is properly installed
- **Solution:** Try Unity-only setup first

### Error Codes
- **Exit Code 1:** System requirements not met
- **Exit Code 2:** Unity installation failed
- **Exit Code 3:** MCP configuration failed
- **Exit Code 4:** Project creation failed

### Getting Help
1. Check error messages in PowerShell output
2. Verify system requirements are met
3. Try individual setup scripts for isolated testing
4. Check Unity Hub and Node.js installations manually

## Development Environment Structure

```
the-search/
├── HOTPPLTheSearch/          # Unity project
│   ├── Assets/               # Game assets
│   ├── Packages/            # Unity packages
│   └── ProjectSettings/     # Unity settings
├── setup-*.ps1             # Setup scripts
├── mcp-config.json          # MCP configuration
├── package.json             # Node.js dependencies
├── start-development.ps1    # Development launcher
└── logs/                    # MCP server logs
```

## Next Steps After Setup

1. **Familiarize with Unity Project:**
   - Open project using desktop shortcut
   - Explore the pre-configured asset structure
   - Review character system documentation

2. **Start Development:**
   - Use MCP integration for automated coordination
   - Follow the development phases in HOT PPL.txt
   - Utilize character asset system for main trio

3. **Customize Configuration:**
   - Adjust MCP server settings as needed
   - Configure performance thresholds
   - Set up additional automation rules

## Advanced Configuration

### Custom MCP Servers
Add custom servers to `mcp-config.json`:
```json
{
  "mcpServers": {
    "custom-server": {
      "command": "node",
      "args": ["custom-server.js"],
      "description": "Custom development server"
    }
  }
}
```

### Unity Package Management
Modify package manifest in `HOTPPLTheSearch/Packages/manifest.json` to add additional packages.

### Performance Tuning
Adjust monitoring thresholds in MCP configuration:
```json
{
  "alertThresholds": {
    "minFPS": 60,
    "maxMemoryMB": 512,
    "maxDrawCalls": 300
  }
}
```

This setup system provides a complete foundation for autonomous game development following the HOT PPL: The Search development plan.
