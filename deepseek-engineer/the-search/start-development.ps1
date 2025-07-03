# HOT PPL: The Search - Development Environment Startup
# This script starts all development tools and MCP servers

Write-Host @"
================================================================
                HOT PPL: The Search
              Development Environment
================================================================
"@ -ForegroundColor Cyan

# Check if Node.js is available
try {
    $nodeVersion = node --version
    Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Error "Node.js not found. Please install Node.js to run MCP servers."
    exit 1
}

# Install dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install dependencies"
        exit 1
    }
}

# Start MCP servers using the main launcher
Write-Host "Starting MCP servers..." -ForegroundColor Yellow
Start-Process -FilePath "node" -ArgumentList "index.js" -WindowStyle Minimized

# Wait for servers to start
Start-Sleep -Seconds 5

# Open Unity project
Write-Host "Opening Unity project..." -ForegroundColor Yellow
$unityExe = "C:\Program Files\Unity\Hub\Editor\6000.1.9f1\Editor\Unity.exe"
$unityHub = "C:\Program Files\Unity Hub\Unity Hub.exe"
$projectPath = ".\HOTPPLTheSearch"

if (Test-Path $unityHub) {
    Write-Host "Opening project via Unity Hub..." -ForegroundColor Green
    Start-Process -FilePath $unityHub -ArgumentList "-- --projectPath `"$(Resolve-Path $projectPath)`""
} elseif (Test-Path $unityExe) {
    Write-Host "Opening project directly..." -ForegroundColor Green
    Start-Process -FilePath $unityExe -ArgumentList "-projectPath", $projectPath
} else {
    Write-Warning "Unity not found. Please open the project manually."
    Write-Host "Project path: $(Resolve-Path $projectPath)" -ForegroundColor Gray
}

Write-Host @"

=== Development Environment Started! ===

MCP Servers Running:
- Unity Integration Server
- Git Integration Server
- Task Management Server
- Performance Monitoring Server

Unity Project: HOTPPLTheSearch
Unity Version: 6000.1.9f1 (Unity 6)

Next Steps:
1. Unity should be opening with your project
2. Use Unity's console or external MCP clients to interact with servers
3. Check server logs for any issues

"@ -ForegroundColor Green

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
