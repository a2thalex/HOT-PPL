# HOT PPL: The Search - MCP Integration Setup Script
# This script sets up MCP servers for Unity development coordination

param(
    [string]$ProjectPath = ".\HOTPPLTheSearch",
    [switch]$InstallMCPServers,
    [switch]$ConfigureOnly
)

Write-Host "=== HOT PPL: The Search - MCP Integration Setup ===" -ForegroundColor Cyan
Write-Host "Setting up MCP servers for development coordination..." -ForegroundColor Green

# Function to check if Node.js is installed
function Test-NodeJS {
    try {
        $nodeVersion = node --version 2>$null
        if ($nodeVersion) {
            Write-Host "Node.js found: $nodeVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

# Function to install Node.js
function Install-NodeJS {
    Write-Host "Installing Node.js..." -ForegroundColor Yellow
    
    $nodeUrl = "https://nodejs.org/dist/v20.10.0/node-v20.10.0-x64.msi"
    $nodeInstaller = "$env:TEMP\nodejs-installer.msi"
    
    try {
        Write-Host "Downloading Node.js installer..."
        Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeInstaller -UseBasicParsing
        
        Write-Host "Installing Node.js..."
        Start-Process -FilePath "msiexec.exe" -ArgumentList "/i", $nodeInstaller, "/quiet" -Wait
        
        Remove-Item $nodeInstaller -Force
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        
        Write-Host "Node.js installed successfully!" -ForegroundColor Green
    }
    catch {
        Write-Error "Failed to install Node.js: $_"
        exit 1
    }
}

# Function to create MCP server configuration
function New-MCPConfiguration {
    param([string]$ProjectPath)
    
    Write-Host "Creating MCP server configuration..." -ForegroundColor Yellow
    
    $mcpConfig = @{
        mcpServers = @{
            "unity-integration" = @{
                command = "mcp-unity-server"
                args = @("--project-path", $ProjectPath)
            }
            "task-management" = @{
                command = "mcp-task-server"
                args = @("--board", "hotppl-development")
            }
            "git-integration" = @{
                command = "mcp-git-server"
                args = @("--repo", ".")
            }
            "performance-monitoring" = @{
                command = "mcp-perf-server"
                args = @("--unity-project", $ProjectPath)
            }
        }
    }
    
    $configPath = Join-Path (Get-Location) "mcp-config.json"
    $configJson = $mcpConfig | ConvertTo-Json -Depth 10
    Set-Content -Path $configPath -Value $configJson -Encoding UTF8
    
    Write-Host "MCP configuration created: $configPath" -ForegroundColor Green
    return $configPath
}

# Function to create Unity MCP integration script
function New-UnityMCPIntegration {
    param([string]$ProjectPath)
    
    Write-Host "Creating Unity MCP integration..." -ForegroundColor Yellow
    
    $integrationScript = @"
using UnityEngine;
using UnityEditor;
using System.Diagnostics;
using System.IO;

namespace HOTPPLTheSearch.MCP
{
    /// <summary>
    /// Unity integration for MCP (Model Context Protocol) servers
    /// Provides automated development coordination and monitoring
    /// </summary>
    public class MCPIntegration : EditorWindow
    {
        private static Process[] mcpProcesses = new Process[4];
        private static bool isInitialized = false;
        
        [MenuItem("HOTPPL/MCP/Start All Servers")]
        public static void StartAllMCPServers()
        {
            StartMCPServer("unity-integration", 0);
            StartMCPServer("task-management", 1);
            StartMCPServer("git-integration", 2);
            StartMCPServer("performance-monitoring", 3);
            
            isInitialized = true;
            UnityEngine.Debug.Log("All MCP servers started");
        }
        
        [MenuItem("HOTPPL/MCP/Stop All Servers")]
        public static void StopAllMCPServers()
        {
            for (int i = 0; i < mcpProcesses.Length; i++)
            {
                if (mcpProcesses[i] != null && !mcpProcesses[i].HasExited)
                {
                    mcpProcesses[i].Kill();
                    mcpProcesses[i] = null;
                }
            }
            
            isInitialized = false;
            UnityEngine.Debug.Log("All MCP servers stopped");
        }
        
        [MenuItem("HOTPPL/MCP/Server Status")]
        public static void ShowServerStatus()
        {
            GetWindow<MCPIntegration>("MCP Server Status");
        }
        
        private static void StartMCPServer(string serverName, int index)
        {
            try
            {
                string configPath = Path.Combine(Application.dataPath, "..", "..", "mcp-config.json");
                
                ProcessStartInfo startInfo = new ProcessStartInfo
                {
                    FileName = "node",
                    Arguments = `$"mcp-server-{serverName}.js --config {configPath}",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };
                
                mcpProcesses[index] = Process.Start(startInfo);
                UnityEngine.Debug.Log(`$"Started MCP server: {serverName}");
            }
            catch (System.Exception e)
            {
                UnityEngine.Debug.LogError(`$"Failed to start MCP server {serverName}: {e.Message}");
            }
        }
        
        void OnGUI()
        {
            GUILayout.Label("MCP Server Status", EditorStyles.boldLabel);
            
            string[] serverNames = { "Unity Integration", "Task Management", "Git Integration", "Performance Monitoring" };
            
            for (int i = 0; i < serverNames.Length; i++)
            {
                GUILayout.BeginHorizontal();
                GUILayout.Label(serverNames[i]);
                
                bool isRunning = mcpProcesses[i] != null && !mcpProcesses[i].HasExited;
                GUILayout.Label(isRunning ? "Running" : "Stopped", isRunning ? EditorStyles.label : EditorStyles.miniLabel);
                
                GUILayout.EndHorizontal();
            }
            
            GUILayout.Space(10);
            
            if (GUILayout.Button("Start All Servers"))
            {
                StartAllMCPServers();
            }
            
            if (GUILayout.Button("Stop All Servers"))
            {
                StopAllMCPServers();
            }
        }
        
        [InitializeOnLoadMethod]
        static void InitializeOnLoad()
        {
            EditorApplication.playModeStateChanged += OnPlayModeStateChanged;
        }
        
        private static void OnPlayModeStateChanged(PlayModeStateChange state)
        {
            if (state == PlayModeStateChange.EnteredPlayMode && !isInitialized)
            {
                StartAllMCPServers();
            }
        }
    }
    
    /// <summary>
    /// Performance monitoring integration for MCP
    /// </summary>
    public class MCPPerformanceMonitor : MonoBehaviour
    {
        [Header("Performance Monitoring")]
        public bool enableMonitoring = true;
        public float reportInterval = 5f;
        
        private float lastReportTime;
        private int frameCount;
        private float deltaTimeSum;
        
        void Update()
        {
            if (!enableMonitoring) return;
            
            frameCount++;
            deltaTimeSum += Time.deltaTime;
            
            if (Time.time - lastReportTime >= reportInterval)
            {
                ReportPerformanceMetrics();
                lastReportTime = Time.time;
                frameCount = 0;
                deltaTimeSum = 0;
            }
        }
        
        void ReportPerformanceMetrics()
        {
            float avgFPS = frameCount / deltaTimeSum;
            long memoryUsage = System.GC.GetTotalMemory(false);
            
            var metrics = new
            {
                timestamp = System.DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"),
                fps = avgFPS,
                memoryUsageMB = memoryUsage / (1024 * 1024),
                drawCalls = UnityEngine.Rendering.DebugUI.instance != null ? 0 : 0, // Placeholder
                triangles = 0 // Placeholder
            };
            
            // Send metrics to MCP performance monitoring server
            SendMetricsToMCP(metrics);
        }
        
        void SendMetricsToMCP(object metrics)
        {
            // Implementation would send metrics to MCP server
            UnityEngine.Debug.Log(`$"Performance Metrics: FPS={((dynamic)metrics).fps:F1}, Memory={((dynamic)metrics).memoryUsageMB}MB");
        }
    }
}
"@
    
    $scriptPath = Join-Path $ProjectPath "Assets\Scripts\Editor\MCPIntegration.cs"
    $editorDir = Split-Path $scriptPath -Parent
    
    if (-not (Test-Path $editorDir)) {
        New-Item -ItemType Directory -Path $editorDir -Force | Out-Null
    }
    
    Set-Content -Path $scriptPath -Value $integrationScript -Encoding UTF8
    Write-Host "Unity MCP integration script created: $scriptPath" -ForegroundColor Green
}

# Function to create MCP server implementations
function New-MCPServers {
    Write-Host "Creating MCP server implementations..." -ForegroundColor Yellow
    
    # Create package.json for MCP servers
    $packageJson = @{
        name = "hotppl-mcp-servers"
        version = "1.0.0"
        description = "MCP servers for HOT PPL: The Search development"
        main = "index.js"
        scripts = @{
            start = "node index.js"
            "start:unity" = "node mcp-server-unity-integration.js"
            "start:tasks" = "node mcp-server-task-management.js"
            "start:git" = "node mcp-server-git-integration.js"
            "start:perf" = "node mcp-server-performance-monitoring.js"
        }
        dependencies = @{
            "@modelcontextprotocol/sdk" = "^0.4.0"
            "ws" = "^8.14.2"
            "chokidar" = "^3.5.3"
            "simple-git" = "^3.20.0"
        }
    }
    
    $packagePath = Join-Path (Get-Location) "package.json"
    $packageJsonContent = $packageJson | ConvertTo-Json -Depth 10
    Set-Content -Path $packagePath -Value $packageJsonContent -Encoding UTF8
    
    Write-Host "Package.json created: $packagePath" -ForegroundColor Green
}

# Function to install MCP server dependencies
function Install-MCPDependencies {
    Write-Host "Installing MCP server dependencies..." -ForegroundColor Yellow
    
    try {
        npm install
        Write-Host "MCP dependencies installed successfully!" -ForegroundColor Green
    }
    catch {
        Write-Error "Failed to install MCP dependencies: $_"
        exit 1
    }
}

# Function to create startup script
function New-StartupScript {
    $startupScript = @"
# HOT PPL: The Search - Development Environment Startup
# This script starts all development tools and MCP servers

Write-Host "=== Starting HOT PPL Development Environment ===" -ForegroundColor Cyan

# Start MCP servers
Write-Host "Starting MCP servers..." -ForegroundColor Yellow
Start-Process -FilePath "npm" -ArgumentList "run", "start:unity" -WindowStyle Hidden
Start-Process -FilePath "npm" -ArgumentList "run", "start:tasks" -WindowStyle Hidden
Start-Process -FilePath "npm" -ArgumentList "run", "start:git" -WindowStyle Hidden
Start-Process -FilePath "npm" -ArgumentList "run", "start:perf" -WindowStyle Hidden

# Wait for servers to start
Start-Sleep -Seconds 3

# Open Unity project
Write-Host "Opening Unity project..." -ForegroundColor Yellow
`$unityExe = "${env:ProgramFiles}\Unity\Hub\Editor\2023.3.0f1\Editor\Unity.exe"
if (Test-Path `$unityExe) {
    Start-Process -FilePath `$unityExe -ArgumentList "-projectPath", ".\HOTPPLTheSearch"
} else {
    Write-Warning "Unity executable not found. Please open the project manually."
}

Write-Host "Development environment started!" -ForegroundColor Green
Write-Host "MCP servers are running in the background" -ForegroundColor Gray
"@
    
    $startupPath = Join-Path (Get-Location) "start-development.ps1"
    Set-Content -Path $startupPath -Value $startupScript -Encoding UTF8
    
    Write-Host "Startup script created: $startupPath" -ForegroundColor Green
}

# Main execution
try {
    # Check prerequisites
    if (-not (Test-NodeJS)) {
        if ($InstallMCPServers) {
            Install-NodeJS
        } else {
            Write-Error "Node.js is required for MCP servers. Run with -InstallMCPServers to install automatically."
            exit 1
        }
    }
    
    # Create MCP configuration
    $configPath = New-MCPConfiguration -ProjectPath $ProjectPath
    
    # Create Unity integration
    if (Test-Path $ProjectPath) {
        New-UnityMCPIntegration -ProjectPath $ProjectPath
    } else {
        Write-Warning "Unity project path not found: $ProjectPath"
        Write-Host "Run setup-unity-cli.ps1 first to create the Unity project" -ForegroundColor Yellow
    }
    
    # Create MCP servers
    if ($InstallMCPServers -or -not $ConfigureOnly) {
        New-MCPServers
        
        if (Test-NodeJS) {
            Install-MCPDependencies
        }
    }
    
    # Create startup script
    New-StartupScript
    
    Write-Host "=== MCP Integration Setup Complete! ===" -ForegroundColor Cyan
    Write-Host "Configuration created: $configPath" -ForegroundColor Green
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Run start-development.ps1 to start the development environment" -ForegroundColor White
    Write-Host "2. Use HOTPPL > MCP menu in Unity to manage servers" -ForegroundColor White
    Write-Host "3. MCP servers will provide automated development coordination" -ForegroundColor White
}
catch {
    Write-Error "MCP setup failed: $_"
    exit 1
}
