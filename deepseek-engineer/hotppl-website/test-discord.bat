@echo off
REM HOT PPL Discord Test Script
REM Quick test of Discord bot functionality

echo.
echo 🧪 Testing HOT PPL Discord Integration
echo.

REM Check if environment is configured
if not exist ".env" (
    echo ❌ .env file not found!
    echo Run deploy-discord.bat first
    pause
    exit /b 1
)

REM Test Discord connection
echo 🔍 Testing Discord connection...
python discord-cli.py stats
if %errorlevel% neq 0 (
    echo ❌ Discord connection failed!
    echo Check your bot token and guild ID
    pause
    exit /b 1
)

echo ✅ Discord connection working

REM Test sending announcement
echo.
echo 📢 Testing announcement...
python discord-cli.py announce --message "🛸 HOT PPL Discord bot test - all systems operational!"
if %errorlevel% equ 0 (
    echo ✅ Announcement sent successfully
) else (
    echo ⚠️ Announcement failed (check bot permissions)
)

REM Test submission
echo.
echo 🎬 Testing submission...
python discord-cli.py submit --creator "TestUser" --scene "The Arrival" --description "Test submission from deployment script"
if %errorlevel% equ 0 (
    echo ✅ Test submission posted
) else (
    echo ⚠️ Submission failed (check channels exist)
)

REM Test leaderboard
echo.
echo 🏆 Testing leaderboard...
python discord-cli.py leaderboard
if %errorlevel% equ 0 (
    echo ✅ Leaderboard updated
) else (
    echo ⚠️ Leaderboard failed
)

echo.
echo 🎉 Discord integration test complete!
echo.
echo If all tests passed, your Discord bot is ready!
echo If any failed, check the error messages above.
echo.

pause
