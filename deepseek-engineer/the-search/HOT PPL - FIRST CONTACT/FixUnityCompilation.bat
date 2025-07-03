@echo off
title Unity Compilation Fix - HOT PPL First Contact
color 0A

echo ===============================================
echo    Unity Compilation Fix Script
echo    Resolving Assembly Resolution Issues
echo ===============================================
echo.

echo [1/5] Checking for Unity processes...
tasklist /FI "IMAGENAME eq Unity.exe" 2>NUL | find /I /N "Unity.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo WARNING: Unity is currently running!
    echo Please close Unity before continuing.
    echo.
    pause
    goto :check_unity
)

:check_unity
tasklist /FI "IMAGENAME eq Unity.exe" 2>NUL | find /I /N "Unity.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Unity is still running. Please close it and press any key...
    pause >nul
    goto :check_unity
)

echo Unity is not running. Proceeding...
echo.

echo [2/5] Creating backup...
set BACKUP_DIR=Backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%
mkdir "%BACKUP_DIR%" 2>nul
copy "Packages\manifest.json" "%BACKUP_DIR%\manifest.json.backup" >nul 2>&1
xcopy "ProjectSettings" "%BACKUP_DIR%\ProjectSettings\" /E /I /Q >nul 2>&1
echo Backup created in %BACKUP_DIR%
echo.

echo [3/5] Clearing Unity cache folders...
if exist "Library" (
    echo Deleting Library folder...
    rmdir /s /q "Library" 2>nul
    if exist "Library" (
        echo WARNING: Could not delete Library folder completely
        echo You may need to delete it manually
    ) else (
        echo Library folder deleted successfully
    )
) else (
    echo Library folder not found (normal for new projects)
)

if exist "Temp" (
    echo Deleting Temp folder...
    rmdir /s /q "Temp" 2>nul
)

if exist "Logs" (
    echo Deleting Logs folder...
    rmdir /s /q "Logs" 2>nul
)
echo.

echo [4/5] Verifying project files...
if exist "Assets\Scripts\HOTPPLRuntime.asmdef" (
    echo Assembly definition file found
) else (
    echo WARNING: Assembly definition file missing
    echo This should have been created by the setup script
)

if exist "Packages\manifest.json" (
    echo Package manifest found
) else (
    echo ERROR: Package manifest missing!
)
echo.

echo [5/5] Compilation fix complete!
echo.
echo ===============================================
echo                NEXT STEPS
echo ===============================================
echo.
echo 1. Open Unity Hub
echo 2. Open this project
echo 3. Wait for Unity to import assets and compile
echo 4. Check Console window for any errors
echo 5. If errors persist, try "Assets > Reimport All"
echo.
echo KEY CHANGES MADE:
echo - Removed problematic AI packages
echo - Added essential Unity packages
echo - Created assembly definition file
echo - Cleared all cached data
echo.
echo If you need to restore files, check the %BACKUP_DIR% folder
echo.
echo Press any key to exit...
pause >nul
