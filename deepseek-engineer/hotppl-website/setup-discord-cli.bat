@echo off
REM HOT PPL Discord CLI Setup Script for Windows
REM Sets up Discord CLI tools for HOT PPL platform

echo.
echo 🛸 HOT PPL Discord CLI Setup
echo Setting up Discord CLI tools for HOT PPL platform...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo ✅ pip found

REM Install Python dependencies
echo.
echo 📦 Installing Python dependencies...
pip install discord.py requests aiohttp python-dotenv flask

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Python dependencies installed

REM Check if Node.js is installed (optional)
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Node.js found
    echo 📦 Installing optional Node.js tools...
    npm install -g discord-cli-tools 2>nul || echo ⚠️ discord-cli-tools installation failed (optional)
) else (
    echo ⚠️ Node.js not found (optional for additional tools)
    echo You can install it from https://nodejs.org/
)

REM Create environment file
echo.
echo ⚙️ Creating environment configuration...

if not exist .env (
    echo # HOT PPL Discord Configuration > .env
    echo # Get these values from Discord Developer Portal >> .env
    echo. >> .env
    echo # Discord Bot Token (from Bot section) >> .env
    echo DISCORD_BOT_TOKEN=your_bot_token_here >> .env
    echo. >> .env
    echo # Discord Server (Guild) ID >> .env
    echo DISCORD_GUILD_ID=your_guild_id_here >> .env
    echo. >> .env
    echo # Discord OAuth2 (from OAuth2 section) >> .env
    echo DISCORD_CLIENT_ID=your_client_id_here >> .env
    echo DISCORD_CLIENT_SECRET=your_client_secret_here >> .env
    echo DISCORD_REDIRECT_URI=https://hotppl.io/auth/discord >> .env
    echo. >> .env
    echo # Discord Webhook URL (for notifications) >> .env
    echo DISCORD_WEBHOOK_URL=your_webhook_url_here >> .env
    echo. >> .env
    echo # Flask configuration >> .env
    echo FLASK_SECRET_KEY=your_flask_secret_key_here >> .env
    
    echo ✅ Created .env file
    echo ⚠️ Please edit .env file with your Discord credentials
) else (
    echo ⚠️ .env file already exists
)

REM Create batch files for easy CLI access
echo.
echo 🔗 Creating CLI shortcuts...

REM Discord CLI shortcuts
echo @echo off > hotppl-setup.bat
echo python discord-cli.py setup >> hotppl-setup.bat

echo @echo off > hotppl-stats.bat
echo python discord-cli.py stats >> hotppl-stats.bat

echo @echo off > hotppl-announce.bat
echo python discord-cli.py announce --message "%%*" >> hotppl-announce.bat

echo @echo off > hotppl-submit.bat
echo python discord-cli.py submit %%* >> hotppl-submit.bat

echo @echo off > hotppl-leaderboard.bat
echo python discord-cli.py leaderboard >> hotppl-leaderboard.bat

REM Bot and API starters
echo @echo off > start-discord-bot.bat
echo echo Starting HOT PPL Discord Bot... >> start-discord-bot.bat
echo python discord-bot.py >> start-discord-bot.bat

echo @echo off > start-discord-api.bat
echo echo Starting HOT PPL Discord API... >> start-discord-api.bat
echo python discord-api.py >> start-discord-api.bat

echo ✅ Created CLI shortcuts

REM Create Discord bot setup guide
echo.
echo 📖 Creating setup guide...

echo # 🤖 Discord Bot Setup Guide > DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo ## Step 1: Create Discord Application >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo 1. Go to [Discord Developer Portal](https://discord.com/developers/applications) >> DISCORD-BOT-SETUP.md
echo 2. Click "New Application" >> DISCORD-BOT-SETUP.md
echo 3. Name it "HOT PPL Bot" >> DISCORD-BOT-SETUP.md
echo 4. Save the **Application ID** (this is your CLIENT_ID) >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo ## Step 2: Create Bot >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo 1. Go to "Bot" section in your application >> DISCORD-BOT-SETUP.md
echo 2. Click "Add Bot" >> DISCORD-BOT-SETUP.md
echo 3. Copy the **Token** (this is your BOT_TOKEN) >> DISCORD-BOT-SETUP.md
echo 4. Enable required permissions >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo ## Step 3: Get Server ID >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo 1. Enable Developer Mode in Discord >> DISCORD-BOT-SETUP.md
echo 2. Right-click your server name >> DISCORD-BOT-SETUP.md
echo 3. Click "Copy ID" (this is your GUILD_ID) >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo ## Step 4: Update .env File >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo Edit the `.env` file with your actual values >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo ## Step 5: Test the Bot >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo ```bash >> DISCORD-BOT-SETUP.md
echo # Test basic connection >> DISCORD-BOT-SETUP.md
echo hotppl-stats.bat >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo # Set up server structure >> DISCORD-BOT-SETUP.md
echo hotppl-setup.bat >> DISCORD-BOT-SETUP.md
echo. >> DISCORD-BOT-SETUP.md
echo # Send test announcement >> DISCORD-BOT-SETUP.md
echo hotppl-announce.bat "HOT PPL bot is online! 🛸" >> DISCORD-BOT-SETUP.md
echo ``` >> DISCORD-BOT-SETUP.md

echo ✅ Created Discord bot setup guide

REM Create PowerShell version for advanced users
echo.
echo 🔧 Creating PowerShell CLI...

echo # HOT PPL Discord PowerShell CLI > discord-cli.ps1
echo # Load environment variables >> discord-cli.ps1
echo if (Test-Path .env) { >> discord-cli.ps1
echo     Get-Content .env ^| ForEach-Object { >> discord-cli.ps1
echo         if ($_ -match '^([^#].*)=(.*)$') { >> discord-cli.ps1
echo             [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) >> discord-cli.ps1
echo         } >> discord-cli.ps1
echo     } >> discord-cli.ps1
echo } >> discord-cli.ps1
echo. >> discord-cli.ps1
echo # Discord CLI functions >> discord-cli.ps1
echo function Start-HotPPLBot { python discord-bot.py } >> discord-cli.ps1
echo function Start-HotPPLAPI { python discord-api.py } >> discord-cli.ps1
echo function Get-HotPPLStats { python discord-cli.py stats } >> discord-cli.ps1
echo function Set-HotPPLServer { python discord-cli.py setup } >> discord-cli.ps1
echo function Send-HotPPLAnnouncement { param($message) python discord-cli.py announce --message "$message" } >> discord-cli.ps1

echo ✅ Created PowerShell CLI

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Read DISCORD-BOT-SETUP.md for Discord configuration
echo 2. Edit .env file with your Discord credentials
echo 3. Test with: hotppl-stats.bat
echo.
echo Available commands:
echo   hotppl-setup.bat         - Set up Discord server
echo   hotppl-stats.bat         - Show server statistics  
echo   hotppl-announce.bat      - Send announcement
echo   hotppl-submit.bat        - Submit new content
echo   hotppl-leaderboard.bat   - Update leaderboard
echo   start-discord-bot.bat    - Start Discord bot
echo   start-discord-api.bat    - Start API server
echo.
echo 🛸 HOT PPL Discord CLI is ready to rock!
echo.
pause
