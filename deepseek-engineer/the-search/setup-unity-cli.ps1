# HOT PPL: The Search - Unity CLI Setup Script
# This script installs Unity 2023.3 LTS and sets up the project structure

param(
    [switch]$SkipUnityInstall,
    [switch]$SkipProjectSetup,
    [string]$UnityVersion = "2023.3.0f1",
    [string]$ProjectName = "HOTPPLTheSearch"
)

Write-Host "=== HOT PPL: The Search - Unity Setup ===" -ForegroundColor Cyan
Write-Host "Setting up Unity 2023.3 LTS and project structure..." -ForegroundColor Green

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Warning "This script should be run as Administrator for Unity installation"
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 1
    }
}

# Function to check if Unity Hub is installed
function Test-UnityHub {
    $hubPath = Get-Command "Unity Hub" -ErrorAction SilentlyContinue
    if ($hubPath) {
        return $true
    }
    
    # Check common installation paths
    $commonPaths = @(
        "${env:ProgramFiles}\Unity Hub\Unity Hub.exe",
        "${env:ProgramFiles(x86)}\Unity Hub\Unity Hub.exe",
        "${env:LOCALAPPDATA}\Programs\Unity Hub\Unity Hub.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            return $true
        }
    }
    
    return $false
}

# Function to install Unity Hub
function Install-UnityHub {
    Write-Host "Installing Unity Hub..." -ForegroundColor Yellow
    
    $hubUrl = "https://public-cdn.cloud.unity3d.com/hub/prod/UnityHubSetup.exe"
    $hubInstaller = "$env:TEMP\UnityHubSetup.exe"
    
    try {
        Write-Host "Downloading Unity Hub installer..."
        Invoke-WebRequest -Uri $hubUrl -OutFile $hubInstaller -UseBasicParsing
        
        Write-Host "Running Unity Hub installer..."
        Start-Process -FilePath $hubInstaller -ArgumentList "/S" -Wait
        
        Remove-Item $hubInstaller -Force
        Write-Host "Unity Hub installed successfully!" -ForegroundColor Green
    }
    catch {
        Write-Error "Failed to install Unity Hub: $_"
        exit 1
    }
}

# Function to install Unity Editor
function Install-UnityEditor {
    param([string]$Version)
    
    Write-Host "Installing Unity Editor $Version..." -ForegroundColor Yellow
    
    # Find Unity Hub executable
    $hubExe = $null
    $commonPaths = @(
        "${env:ProgramFiles}\Unity Hub\Unity Hub.exe",
        "${env:ProgramFiles(x86)}\Unity Hub\Unity Hub.exe",
        "${env:LOCALAPPDATA}\Programs\Unity Hub\Unity Hub.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $hubExe = $path
            break
        }
    }
    
    if (-not $hubExe) {
        Write-Error "Unity Hub executable not found"
        exit 1
    }
    
    # Install Unity Editor with required modules
    $modules = @(
        "windows-il2cpp",
        "universal-windows-platform",
        "webgl",
        "android",
        "documentation",
        "language-pack-en"
    )
    
    $moduleArgs = $modules -join ","
    
    try {
        Write-Host "Installing Unity $Version with modules: $moduleArgs"
        & "$hubExe" -- --headless install --version $Version --module $moduleArgs
        
        Write-Host "Unity Editor $Version installed successfully!" -ForegroundColor Green
    }
    catch {
        Write-Error "Failed to install Unity Editor: $_"
        exit 1
    }
}

# Function to create Unity project
function New-UnityProject {
    param(
        [string]$ProjectName,
        [string]$ProjectPath,
        [string]$UnityVersion
    )
    
    Write-Host "Creating Unity project: $ProjectName" -ForegroundColor Yellow
    
    # Find Unity Editor executable
    $unityExe = "${env:ProgramFiles}\Unity\Hub\Editor\$UnityVersion\Editor\Unity.exe"
    if (-not (Test-Path $unityExe)) {
        $unityExe = "${env:ProgramFiles(x86)}\Unity\Hub\Editor\$UnityVersion\Editor\Unity.exe"
    }
    
    if (-not (Test-Path $unityExe)) {
        Write-Error "Unity Editor executable not found for version $UnityVersion"
        exit 1
    }
    
    try {
        # Create project using Unity CLI
        $args = @(
            "-createProject", $ProjectPath,
            "-projectTemplate", "3D",
            "-quit",
            "-batchmode",
            "-nographics"
        )
        
        Write-Host "Running Unity to create project..."
        & $unityExe $args
        
        Write-Host "Unity project created successfully!" -ForegroundColor Green
    }
    catch {
        Write-Error "Failed to create Unity project: $_"
        exit 1
    }
}

# Function to setup project structure
function Initialize-ProjectStructure {
    param([string]$ProjectPath)
    
    Write-Host "Setting up project structure..." -ForegroundColor Yellow
    
    $folders = @(
        "Assets\Scripts",
        "Assets\Scripts\Character",
        "Assets\Scripts\Vehicle", 
        "Assets\Scripts\Social",
        "Assets\Scripts\UI",
        "Assets\Scripts\Networking",
        "Assets\Scripts\Progression",
        "Assets\Scripts\Audio",
        "Assets\Art",
        "Assets\Art\Characters",
        "Assets\Art\Characters\Models",
        "Assets\Art\Characters\Textures",
        "Assets\Art\Characters\Materials",
        "Assets\Art\Characters\Animations",
        "Assets\Art\Vehicles",
        "Assets\Art\Environment",
        "Assets\Audio",
        "Assets\Audio\Music",
        "Assets\Audio\SFX",
        "Assets\Audio\Voice",
        "Assets\Scenes",
        "Assets\Prefabs",
        "Assets\Prefabs\Characters",
        "Assets\Prefabs\Vehicles",
        "Assets\Prefabs\UI",
        "Assets\Materials",
        "Assets\Resources",
        "Assets\Data",
        "Assets\Data\Characters",
        "Assets\Data\Clothing",
        "Assets\Data\Vehicles"
    )
    
    foreach ($folder in $folders) {
        $fullPath = Join-Path $ProjectPath $folder
        if (-not (Test-Path $fullPath)) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
            Write-Host "Created: $folder" -ForegroundColor Gray
        }
    }
    
    Write-Host "Project structure created successfully!" -ForegroundColor Green
}

# Function to install required Unity packages
function Install-UnityPackages {
    param([string]$ProjectPath)
    
    Write-Host "Installing required Unity packages..." -ForegroundColor Yellow
    
    # Create manifest.json with required packages
    $manifestPath = Join-Path $ProjectPath "Packages\manifest.json"
    $manifest = @{
        dependencies = @{
            "com.unity.inputsystem" = "1.7.0"
            "com.unity.cinemachine" = "2.9.7"
            "com.unity.timeline" = "1.7.6"
            "com.unity.render-pipelines.universal" = "14.0.9"
            "com.unity.textmeshpro" = "3.0.6"
            "com.unity.netcode.gameobjects" = "1.7.1"
            "com.unity.probuilder" = "5.2.2"
            "com.unity.addressables" = "1.21.19"
            "com.unity.postprocessing" = "3.2.2"
            "com.unity.ide.visualstudio" = "2.0.21"
            "com.unity.ide.rider" = "3.0.26"
            "com.unity.test-framework" = "1.1.33"
        }
        scopedRegistries = @()
    }
    
    $manifestJson = $manifest | ConvertTo-Json -Depth 10
    Set-Content -Path $manifestPath -Value $manifestJson -Encoding UTF8
    
    Write-Host "Package manifest updated!" -ForegroundColor Green
}

# Main execution
try {
    # Step 1: Install Unity Hub if not present
    if (-not $SkipUnityInstall) {
        if (-not (Test-UnityHub)) {
            Install-UnityHub
        } else {
            Write-Host "Unity Hub already installed" -ForegroundColor Green
        }
        
        # Step 2: Install Unity Editor
        Install-UnityEditor -Version $UnityVersion
    }
    
    # Step 3: Create Unity project
    if (-not $SkipProjectSetup) {
        $projectPath = Join-Path (Get-Location) $ProjectName
        
        if (Test-Path $projectPath) {
            Write-Warning "Project directory already exists: $projectPath"
            $overwrite = Read-Host "Overwrite existing project? (y/N)"
            if ($overwrite -eq "y" -or $overwrite -eq "Y") {
                Remove-Item $projectPath -Recurse -Force
            } else {
                Write-Host "Skipping project creation" -ForegroundColor Yellow
                exit 0
            }
        }
        
        New-UnityProject -ProjectName $ProjectName -ProjectPath $projectPath -UnityVersion $UnityVersion
        Initialize-ProjectStructure -ProjectPath $projectPath
        Install-UnityPackages -ProjectPath $projectPath
    }
    
    Write-Host "=== Unity Setup Complete! ===" -ForegroundColor Cyan
    Write-Host "Project created at: $(Join-Path (Get-Location) $ProjectName)" -ForegroundColor Green
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Run setup-mcp-integration.ps1 to configure MCP servers" -ForegroundColor White
    Write-Host "2. Open the project in Unity Hub" -ForegroundColor White
    Write-Host "3. Import the character assets from the-search folder" -ForegroundColor White
}
catch {
    Write-Error "Setup failed: $_"
    exit 1
}
