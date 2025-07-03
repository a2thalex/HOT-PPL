# HOT PPL: The Search - Complete Development Environment Setup
# This script sets up the entire development environment including Unity and MCP integration

param(
    [switch]$FullSetup,
    [switch]$UnityOnly,
    [switch]$MCPOnly,
    [switch]$SkipConfirmation,
    [string]$UnityVersion = "2023.3.0f1",
    [string]$ProjectName = "HOTPPLTheSearch"
)

Write-Host @"
================================================================
                    HOT PPL: The Search
              Development Environment Setup

  This script will set up Unity 2023.3 LTS and MCP
  integration for autonomous game development
================================================================
"@ -ForegroundColor Cyan

# Function to check system requirements
function Test-SystemRequirements {
    Write-Host "Checking system requirements..." -ForegroundColor Yellow
    
    $requirements = @{
        "Windows 10/11" = $true
        "PowerShell 5.0+" = ($PSVersionTable.PSVersion.Major -ge 5)
        "Internet Connection" = (Test-Connection -ComputerName "8.8.8.8" -Count 1 -Quiet)
        "Disk Space (10GB+)" = ((Get-WmiObject -Class Win32_LogicalDisk | Where-Object {$_.DeviceID -eq "C:"}).FreeSpace -gt 10GB)
        "Administrator Rights" = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
    }
    
    $allPassed = $true
    foreach ($req in $requirements.GetEnumerator()) {
        $status = if ($req.Value) { "PASS" } else { "FAIL" }
        $color = if ($req.Value) { "Green" } else { "Red" }
        $symbol = if ($req.Value) { "[OK]" } else { "[FAIL]" }
        Write-Host "  $($req.Key): $symbol $status" -ForegroundColor $color

        if (-not $req.Value) {
            $allPassed = $false
        }
    }
    
    if (-not $allPassed) {
        Write-Host "`nSome requirements are not met. Please address the issues above." -ForegroundColor Red
        if (-not $SkipConfirmation) {
            $continue = Read-Host "Continue anyway? (y/N)"
            if ($continue -ne "y" -and $continue -ne "Y") {
                exit 1
            }
        }
    } else {
        Write-Host "`nAll system requirements met!" -ForegroundColor Green
    }
}

# Function to display setup options
function Show-SetupOptions {
    if ($FullSetup -or $UnityOnly -or $MCPOnly) {
        return
    }
    
    Write-Host "`nSetup Options:" -ForegroundColor Yellow
    Write-Host "1. Full Setup (Unity + MCP + Project)" -ForegroundColor White
    Write-Host "2. Unity Only" -ForegroundColor White
    Write-Host "3. MCP Integration Only" -ForegroundColor White
    Write-Host "4. Exit" -ForegroundColor White
    
    do {
        $choice = Read-Host "`nSelect option (1-4)"
        switch ($choice) {
            "1" { $script:FullSetup = $true; break }
            "2" { $script:UnityOnly = $true; break }
            "3" { $script:MCPOnly = $true; break }
            "4" { exit 0 }
            default { Write-Host "Invalid choice. Please select 1-4." -ForegroundColor Red }
        }
    } while (-not ($FullSetup -or $UnityOnly -or $MCPOnly))
}

# Function to setup Unity
function Invoke-UnitySetup {
    Write-Host "`n=== Unity Setup ===" -ForegroundColor Cyan
    
    $scriptPath = Join-Path $PSScriptRoot "setup-unity-cli.ps1"
    if (-not (Test-Path $scriptPath)) {
        Write-Error "Unity setup script not found: $scriptPath"
        return $false
    }
    
    try {
        & $scriptPath -UnityVersion $UnityVersion -ProjectName $ProjectName
        return $true
    }
    catch {
        Write-Error "Unity setup failed: $_"
        return $false
    }
}

# Function to setup MCP integration
function Invoke-MCPSetup {
    Write-Host "`n=== MCP Integration Setup ===" -ForegroundColor Cyan
    
    $scriptPath = Join-Path $PSScriptRoot "setup-mcp-integration.ps1"
    if (-not (Test-Path $scriptPath)) {
        Write-Error "MCP setup script not found: $scriptPath"
        return $false
    }
    
    $projectPath = Join-Path $PSScriptRoot $ProjectName
    
    try {
        & $scriptPath -ProjectPath $projectPath -InstallMCPServers
        return $true
    }
    catch {
        Write-Error "MCP setup failed: $_"
        return $false
    }
}

# Function to copy character assets
function Copy-CharacterAssets {
    Write-Host "`n=== Copying Character Assets ===" -ForegroundColor Cyan
    
    $sourceAssets = Join-Path $PSScriptRoot "Assets"
    $targetAssets = Join-Path $PSScriptRoot "$ProjectName\Assets"
    
    if (Test-Path $sourceAssets) {
        try {
            Write-Host "Copying character assets to Unity project..."
            Copy-Item -Path "$sourceAssets\*" -Destination $targetAssets -Recurse -Force
            Write-Host "Character assets copied successfully!" -ForegroundColor Green
            return $true
        }
        catch {
            Write-Error "Failed to copy character assets: $_"
            return $false
        }
    } else {
        Write-Warning "Character assets not found at: $sourceAssets"
        return $false
    }
}

# Function to create development shortcuts
function New-DevelopmentShortcuts {
    Write-Host "`n=== Creating Development Shortcuts ===" -ForegroundColor Cyan
    
    # Create desktop shortcuts
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $projectPath = Join-Path $PSScriptRoot $ProjectName
    
    # Unity project shortcut
    $unityShortcut = @"
`$WshShell = New-Object -comObject WScript.Shell
`$Shortcut = `$WshShell.CreateShortcut("$desktopPath\HOT PPL Unity.lnk")
`$Shortcut.TargetPath = "${env:ProgramFiles}\Unity\Hub\Unity Hub.exe"
`$Shortcut.Arguments = "-- --projectPath \`"$projectPath\`""
`$Shortcut.WorkingDirectory = "$projectPath"
`$Shortcut.IconLocation = "${env:ProgramFiles}\Unity\Hub\Unity Hub.exe"
`$Shortcut.Description = "Open HOT PPL Unity Project"
`$Shortcut.Save()
"@

    # Development environment shortcut
    $devShortcut = @"
`$WshShell = New-Object -comObject WScript.Shell
`$Shortcut = `$WshShell.CreateShortcut("$desktopPath\HOT PPL Development.lnk")
`$Shortcut.TargetPath = "powershell.exe"
`$Shortcut.Arguments = "-ExecutionPolicy Bypass -File \`"$PSScriptRoot\start-development.ps1\`""
`$Shortcut.WorkingDirectory = "$PSScriptRoot"
`$Shortcut.Description = "Start HOT PPL Development Environment"
`$Shortcut.Save()
"@
    
    try {
        Invoke-Expression $unityShortcut
        Invoke-Expression $devShortcut
        Write-Host "Desktop shortcuts created!" -ForegroundColor Green
    }
    catch {
        Write-Warning "Failed to create desktop shortcuts: $_"
    }
}

# Function to display completion summary
function Show-CompletionSummary {
    param([bool]$UnitySuccess, [bool]$MCPSuccess, [bool]$AssetsSuccess)
    
    Write-Host @"

================================================================
                     Setup Complete!
================================================================
"@ -ForegroundColor Green

    Write-Host "`nSetup Results:" -ForegroundColor Yellow
    Write-Host "  Unity 2023.3 LTS: $(if ($UnitySuccess) { '[OK] Installed' } else { '[FAIL] Failed' })" -ForegroundColor $(if ($UnitySuccess) { 'Green' } else { 'Red' })
    Write-Host "  MCP Integration: $(if ($MCPSuccess) { '[OK] Configured' } else { '[FAIL] Failed' })" -ForegroundColor $(if ($MCPSuccess) { 'Green' } else { 'Red' })
    Write-Host "  Character Assets: $(if ($AssetsSuccess) { '[OK] Copied' } else { '[FAIL] Failed' })" -ForegroundColor $(if ($AssetsSuccess) { 'Green' } else { 'Red' })
    
    Write-Host "`nNext Steps:" -ForegroundColor Yellow
    Write-Host "1. Use 'HOT PPL Development' desktop shortcut to start the environment" -ForegroundColor White
    Write-Host "2. Open Unity project using 'HOT PPL Unity' desktop shortcut" -ForegroundColor White
    Write-Host "3. In Unity, use HOTPPL > MCP menu to manage development servers" -ForegroundColor White
    Write-Host "4. Run CharacterAssetSetup.SetupCharacterAssets() in Unity to initialize assets" -ForegroundColor White
    
    Write-Host "`nProject Location:" -ForegroundColor Yellow
    Write-Host "  $(Join-Path $PSScriptRoot $ProjectName)" -ForegroundColor White
    
    Write-Host "`nDocumentation:" -ForegroundColor Yellow
    Write-Host "  CHARACTER_ASSETS_README.md - Character system documentation" -ForegroundColor White
    Write-Host "  HOT PPL.txt - Complete development plan" -ForegroundColor White
}

# Main execution
try {
    # Check system requirements
    Test-SystemRequirements
    
    # Show setup options
    Show-SetupOptions
    
    # Initialize results
    $unitySuccess = $false
    $mcpSuccess = $false
    $assetsSuccess = $false
    
    # Execute setup based on options
    if ($FullSetup) {
        Write-Host "`nStarting full setup..." -ForegroundColor Green
        $unitySuccess = Invoke-UnitySetup
        $mcpSuccess = Invoke-MCPSetup
        $assetsSuccess = Copy-CharacterAssets
        New-DevelopmentShortcuts
    }
    elseif ($UnityOnly) {
        Write-Host "`nStarting Unity-only setup..." -ForegroundColor Green
        $unitySuccess = Invoke-UnitySetup
        $assetsSuccess = Copy-CharacterAssets
    }
    elseif ($MCPOnly) {
        Write-Host "`nStarting MCP-only setup..." -ForegroundColor Green
        $mcpSuccess = Invoke-MCPSetup
    }
    
    # Show completion summary
    Show-CompletionSummary -UnitySuccess $unitySuccess -MCPSuccess $mcpSuccess -AssetsSuccess $assetsSuccess
    
    # Final prompt
    if (-not $SkipConfirmation) {
        Write-Host "`nPress any key to exit..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}
catch {
    Write-Error "Setup failed: $_"
    Write-Host "`nFor support, check the error messages above and ensure all requirements are met." -ForegroundColor Yellow
    exit 1
}
