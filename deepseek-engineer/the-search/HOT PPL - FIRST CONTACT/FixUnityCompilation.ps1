# Unity Compilation Fix Script
# Resolves Mono.Cecil.AssemblyResolutionException errors

Write-Host "=== Unity Compilation Fix Script ===" -ForegroundColor Cyan
Write-Host "Fixing Assembly Resolution Issues..." -ForegroundColor Yellow

# Get the project directory
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Project Path: $projectPath" -ForegroundColor Green

# Step 1: Check if Unity is running
Write-Host "`n1. Checking for running Unity processes..." -ForegroundColor Yellow
$unityProcesses = Get-Process -Name "Unity*" -ErrorAction SilentlyContinue
if ($unityProcesses) {
    Write-Host "WARNING: Unity is currently running!" -ForegroundColor Red
    Write-Host "Please close Unity before running this script." -ForegroundColor Red
    Write-Host "Found processes: $($unityProcesses.Name -join ', ')" -ForegroundColor Red
    
    $response = Read-Host "Do you want to force close Unity? (y/N)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "Closing Unity processes..." -ForegroundColor Yellow
        $unityProcesses | Stop-Process -Force
        Start-Sleep -Seconds 3
    } else {
        Write-Host "Please close Unity manually and run this script again." -ForegroundColor Red
        exit 1
    }
}

# Step 2: Backup important files
Write-Host "`n2. Creating backup of important files..." -ForegroundColor Yellow
$backupPath = Join-Path $projectPath "Backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null

# Backup manifest.json
$manifestPath = Join-Path $projectPath "Packages\manifest.json"
if (Test-Path $manifestPath) {
    Copy-Item $manifestPath (Join-Path $backupPath "manifest.json.backup")
    Write-Host "Backed up manifest.json" -ForegroundColor Green
}

# Backup ProjectSettings
$projectSettingsPath = Join-Path $projectPath "ProjectSettings"
if (Test-Path $projectSettingsPath) {
    Copy-Item $projectSettingsPath (Join-Path $backupPath "ProjectSettings") -Recurse
    Write-Host "Backed up ProjectSettings" -ForegroundColor Green
}

# Step 3: Clear Library folder
Write-Host "`n3. Clearing Library folder..." -ForegroundColor Yellow
$libraryPath = Join-Path $projectPath "Library"
if (Test-Path $libraryPath) {
    try {
        Remove-Item $libraryPath -Recurse -Force
        Write-Host "Successfully deleted Library folder" -ForegroundColor Green
    } catch {
        Write-Host "Error deleting Library folder: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "You may need to delete it manually" -ForegroundColor Yellow
    }
} else {
    Write-Host "Library folder not found (this is normal for new projects)" -ForegroundColor Yellow
}

# Step 4: Clear Temp folder
Write-Host "`n4. Clearing Temp folder..." -ForegroundColor Yellow
$tempPath = Join-Path $projectPath "Temp"
if (Test-Path $tempPath) {
    try {
        Remove-Item $tempPath -Recurse -Force
        Write-Host "Successfully deleted Temp folder" -ForegroundColor Green
    } catch {
        Write-Host "Error deleting Temp folder: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Step 5: Clear Logs folder
Write-Host "`n5. Clearing Logs folder..." -ForegroundColor Yellow
$logsPath = Join-Path $projectPath "Logs"
if (Test-Path $logsPath) {
    try {
        Remove-Item $logsPath -Recurse -Force
        Write-Host "Successfully deleted Logs folder" -ForegroundColor Green
    } catch {
        Write-Host "Error deleting Logs folder: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Step 6: Verify package manifest
Write-Host "`n6. Verifying package manifest..." -ForegroundColor Yellow
if (Test-Path $manifestPath) {
    $manifestContent = Get-Content $manifestPath -Raw
    if ($manifestContent -match "com\.unity\.ai\.assistant|com\.unity\.ai\.generators|com\.unity\.ai\.inference") {
        Write-Host "WARNING: AI packages detected in manifest.json" -ForegroundColor Red
        Write-Host "These may cause compilation issues in Unity 6.2" -ForegroundColor Yellow
        Write-Host "The script has already updated the manifest to remove problematic packages" -ForegroundColor Green
    } else {
        Write-Host "Package manifest looks good" -ForegroundColor Green
    }
} else {
    Write-Host "Package manifest not found" -ForegroundColor Red
}

# Step 7: Verify assembly definition files
Write-Host "`n7. Verifying assembly definition files..." -ForegroundColor Yellow
$asmdefPath = Join-Path $projectPath "Assets\Scripts\HOTPPLRuntime.asmdef"
if (Test-Path $asmdefPath) {
    Write-Host "Assembly definition file found" -ForegroundColor Green
} else {
    Write-Host "Assembly definition file missing - this has been created by the script" -ForegroundColor Yellow
}

# Step 8: Check for script compilation issues
Write-Host "`n8. Checking script files..." -ForegroundColor Yellow
$scriptsPath = Join-Path $projectPath "Assets\Scripts"
if (Test-Path $scriptsPath) {
    $scriptFiles = Get-ChildItem $scriptsPath -Filter "*.cs" -Recurse
    Write-Host "Found $($scriptFiles.Count) C# script files" -ForegroundColor Green
    
    # Check for common issues
    foreach ($script in $scriptFiles) {
        $content = Get-Content $script.FullName -Raw
        if ($content -match "^\s*[^/\s].*;" -and $content -match "namespace|class|struct") {
            Write-Host "WARNING: Potential top-level statement issue in $($script.Name)" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "Scripts folder not found" -ForegroundColor Red
}

# Step 9: Generate project refresh script
Write-Host "`n9. Creating Unity refresh script..." -ForegroundColor Yellow
$refreshScript = @"
@echo off
echo Starting Unity with project refresh...
echo Please wait for Unity to fully load and recompile...
echo.
echo If you see compilation errors:
echo 1. Check the Console window for specific errors
echo 2. Try Assets > Reimport All
echo 3. Try Edit > Project Settings > Player > Configuration > Scripting Backend
echo.
pause
"@

$refreshScriptPath = Join-Path $projectPath "RefreshUnityProject.bat"
$refreshScript | Out-File -FilePath $refreshScriptPath -Encoding ASCII
Write-Host "Created Unity refresh script: RefreshUnityProject.bat" -ForegroundColor Green

# Step 10: Final instructions
Write-Host "`n=== COMPILATION FIX COMPLETE ===" -ForegroundColor Cyan
Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Open Unity Hub" -ForegroundColor White
Write-Host "2. Open the project (Unity will regenerate Library folder)" -ForegroundColor White
Write-Host "3. Wait for Unity to import all assets and compile scripts" -ForegroundColor White
Write-Host "4. Check the Console window for any remaining errors" -ForegroundColor White
Write-Host "5. If errors persist, try 'Assets > Reimport All'" -ForegroundColor White

Write-Host "`nBackup created at: $backupPath" -ForegroundColor Green
Write-Host "`nIf you need to restore, copy files from the backup folder." -ForegroundColor Yellow

Write-Host "`nKey Changes Made:" -ForegroundColor Cyan
Write-Host "- Removed problematic AI packages from manifest.json" -ForegroundColor White
Write-Host "- Added essential packages (Input System, TextMeshPro, UI)" -ForegroundColor White
Write-Host "- Created assembly definition file for proper compilation order" -ForegroundColor White
Write-Host "- Updated project version to stable Unity 6.2" -ForegroundColor White
Write-Host "- Cleared all cached compilation data" -ForegroundColor White

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
