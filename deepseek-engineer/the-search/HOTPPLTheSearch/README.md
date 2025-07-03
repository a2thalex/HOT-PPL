# HOT PPL: The Search - Unity Project

This is the Unity 6 project for HOT PPL: The Search, integrated with Model Context Protocol (MCP) servers for autonomous game development.

## Project Structure

```
HOTPPLTheSearch/
├── Assets/
│   ├── Characters/          # Character assets and systems
│   ├── Scripts/             # C# scripts
│   │   ├── Editor/          # Unity Editor scripts
│   │   └── MCPIntegration.cs # MCP server integration
│   ├── Art/                 # Art assets
│   ├── Data/                # Game data
│   └── Prefabs/             # Unity prefabs
├── Packages/                # Unity packages
├── ProjectSettings/         # Unity project settings
└── README.md               # This file
```

## MCP Integration

This project includes full MCP (Model Context Protocol) integration with the following servers:

- **Unity Integration Server**: Project monitoring and automation
- **Git Integration Server**: Version control automation  
- **Task Management Server**: Development coordination
- **Performance Monitoring Server**: Real-time performance tracking

### Using MCP in Unity

1. **Unity Menu**: Use `HOTPPL > MCP` menu to start/stop servers
2. **MCPIntegration Component**: Add to a GameObject for runtime control
3. **Editor Scripts**: Custom editor tools for development workflow

### MCP Menu Options

- `HOTPPL > MCP > Start All Servers` - Start all MCP servers
- `HOTPPL > MCP > Stop All Servers` - Stop all MCP servers  
- `HOTPPL > Development > Run Development Environment` - Start full dev environment
- `HOTPPL > Tools > Setup Character Assets` - Initialize character system

## Getting Started

1. **Open Project**: Open this project in Unity 6 (6000.1.9f1 or later)
2. **Start MCP Servers**: Use `HOTPPL > MCP > Start All Servers`
3. **Check Console**: Monitor MCP server status in Unity Console
4. **Begin Development**: Use the integrated tools for development

## Character System

The project includes a character asset system for the main trio:

- **Models**: 3D character models
- **Animations**: Character animations and controllers
- **Textures**: Character textures and materials
- **Prefabs**: Ready-to-use character prefabs

Use `HOTPPL > Tools > Setup Character Assets` to initialize the folder structure.

## Development Workflow

1. **Start Development Environment**: 
   - Run `start-development.ps1` from project root, or
   - Use `HOTPPL > Development > Run Development Environment`

2. **Monitor Performance**:
   - MCP Performance server tracks FPS, memory, draw calls
   - Check Unity Console for performance alerts

3. **Version Control**:
   - MCP Git server provides automated Git operations
   - Commit coordination and branch management

4. **Task Management**:
   - MCP Task server tracks development progress
   - Milestone and dependency management

## Building

Use `HOTPPL > Tools > Build Project` or Unity's standard build process.

Default build location: `../Builds/HOTPPLTheSearch.exe`

## Troubleshooting

### MCP Servers Won't Start
- Ensure Node.js is installed and in PATH
- Check that `npm install` was run in project root
- Verify MCP configuration in `../mcp-config.json`

### Unity Integration Issues
- Check Unity Console for MCP-related errors
- Ensure project path is correct in MCP config
- Try restarting servers via Unity menu

### Performance Issues
- Monitor MCP Performance server output
- Check performance thresholds in MCP config
- Use Unity Profiler for detailed analysis

## Configuration

MCP configuration is stored in `../mcp-config.json` relative to this Unity project.

Key settings:
- Server commands and arguments
- Performance thresholds
- Unity paths and versions
- Alert conditions

## Support

For issues and documentation:
- Check `../SETUP_README.md` for complete setup guide
- Review MCP server logs in project root
- Use `HOTPPL > Help` menu for additional resources

## Version

- Unity Version: 6000.1.9f1 (Unity 6)
- MCP Integration: 1.0.0
- Project Version: 1.0.0
