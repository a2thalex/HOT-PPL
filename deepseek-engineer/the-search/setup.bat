@echo off
REM HOT PPL: The Search - Quick Setup Launcher
REM This batch file launches the PowerShell setup script

echo ===============================================
echo    HOT PPL: The Search - Development Setup
echo ===============================================
echo.

REM Check if PowerShell is available
powershell -Command "Write-Host 'PowerShell is available'" >nul 2>&1p
if errorlevel 1 (
    echo ERROR: PowerShell is not available or not in PATH
    echo Please ensure PowerShell is installed and accessible
    pause
    exit /b 1
)

REM Check if setup script exists
if not exist "setup-hotppl-development.ps1" (
    echo ERROR: Setup script not found
    echo Please ensure setup-hotppl-development.ps1 is in the current directory
    pause
    exit /b 1
)

echo Starting PowerShell setup script...
echo.

REM Run the PowerShell setup script with execution policy bypass
powershell -ExecutionPolicy Bypass -File "setup-hotppl-development.ps1" -FullSetup

if errorlevel 1 (
    echo.
    echo Setup encountered errors. Please check the output above.
    echo.
    echo Troubleshooting tips:
    echo 1. Run as Administrator
    echo 2. Ensure internet connection is available
    echo 3. Check that you have sufficient disk space
    echo 4. Verify Windows version compatibility
    echo.
) else (
    echo.
    echo Setup completed successfully!
    echo You can now start development using the desktop shortcuts.
    echo.
)

echo Press any key to exit...
pause >nul
