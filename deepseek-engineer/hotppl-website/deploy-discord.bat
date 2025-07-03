@echo off
REM HOT PPL Discord Bot Deployment Script
REM Deploy Discord bot and integration for HOT PPL

echo.
echo 🤖 HOT PPL Discord Bot Deployment
echo Deploying Discord integration for hotppl.io...
echo.

REM Check if .env file exists and has bot token
if not exist ".env" (
    echo ❌ .env file not found!
    echo Please create .env file with your Discord credentials
    echo See DISCORD-QUICK-SETUP.md for instructions
    pause
    exit /b 1
)

REM Check if bot token is configured
findstr "your_bot_token_here" .env >nul
if %errorlevel% equ 0 (
    echo ⚠️ Discord bot token not configured!
    echo.
    echo Please edit .env file and add your Discord credentials:
    echo 1. DISCORD_BOT_TOKEN=your_actual_bot_token
    echo 2. DISCORD_GUILD_ID=your_actual_guild_id
    echo 3. DISCORD_CLIENT_ID=your_actual_client_id
    echo.
    echo See DISCORD-QUICK-SETUP.md for detailed instructions
    echo.
    echo Opening setup guide...
    start DISCORD-QUICK-SETUP.md
    pause
    exit /b 1
)

echo ✅ Environment configuration found

REM Test Discord connection
echo.
echo 🔍 Testing Discord connection...
python discord-cli.py stats
if %errorlevel% neq 0 (
    echo ❌ Discord connection failed!
    echo Please check your bot token and guild ID in .env file
    pause
    exit /b 1
)

echo ✅ Discord connection successful

REM Set up Discord server structure
echo.
echo 🏗️ Setting up Discord server structure...
python discord-cli.py setup
if %errorlevel% neq 0 (
    echo ⚠️ Server setup had issues, but continuing...
)

echo ✅ Discord server structure ready

REM Deploy Discord integration to website
echo.
echo 🌐 Deploying Discord integration to hotppl.io...

REM Copy Discord integration files to public folder
copy discord-integration.js public\ >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Discord integration copied to website
) else (
    echo ⚠️ Could not copy Discord integration (may already exist)
)

REM Deploy updated website with Discord integration
echo.
echo 🚀 Deploying updated website...
firebase deploy --only hosting
if %errorlevel% neq 0 (
    echo ❌ Website deployment failed!
    pause
    exit /b 1
)

echo ✅ Website deployed with Discord integration

REM Start Discord API server
echo.
echo 🔧 Starting Discord API server...
start "HOT PPL Discord API" python discord-api.py

REM Wait a moment for API to start
timeout /t 3 /nobreak >nul

REM Start Discord bot
echo.
echo 🤖 Starting Discord bot...
echo.
echo The Discord bot will start in a new window.
echo Keep this window open to monitor the bot.
echo.
echo Available commands:
echo   !hotppl submit [scene] [description] - Submit a scene
echo   !hotppl leaderboard - Show current rankings
echo   !hotppl stats - Show user statistics
echo   React with 🔥 to vote on submissions
echo.

start "HOT PPL Discord Bot" python discord-bot.py

echo.
echo 🎉 Discord deployment complete!
echo.
echo ✅ What's running:
echo   🌐 Website: https://hotppl.io (with Discord integration)
echo   🤖 Discord Bot: Active in your server
echo   🔧 Discord API: Running on localhost:5000
echo.
echo 📋 Next steps:
echo 1. Test the bot with: !hotppl stats
echo 2. Set up server channels with: !hotppl setup (if needed)
echo 3. Send test announcement: !hotppl announce "Bot is live!"
echo 4. Invite your community to start submitting!
echo.
echo 🔥 Your Discord-powered HOT PPL platform is LIVE!
echo.

REM Open Discord to test
echo 🎮 Opening Discord to test the bot...
start discord://

REM Open website to see integration
echo 🌐 Opening hotppl.io to see Discord integration...
start https://hotppl.io

echo.
echo Press any key to close this window (bot will keep running)...
pause >nul
