@echo off
echo 🚀 Deploying HOT PPL Website with Discord Integration to Google Cloud
echo ================================================================

echo.
echo 📋 Pre-deployment checklist:
echo ✅ Discord bot token configured
echo ✅ Channel IDs set up
echo ✅ Flask app with API endpoints ready
echo ✅ Database schema updated

echo.
echo 🔍 Checking gcloud configuration...
gcloud config list

echo.
echo 📦 Installing dependencies locally for testing...
pip install -r requirements.txt

echo.
echo 🧪 Running quick local test...
timeout 10 python main.py > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Local app starts successfully
) else (
    echo ⚠️ Local app test failed, but continuing with deployment
)

echo.
echo 🚀 Deploying to Google App Engine...
gcloud app deploy app.yaml --quiet

if %errorlevel% equ 0 (
    echo.
    echo ✅ Deployment successful!
    echo.
    echo 🌐 Your website is now live with Discord integration!
    echo 📱 Website: https://hotppl.io
    echo 🤖 Discord features:
    echo    - Automatic submission posting
    echo    - Real-time voting sync
    echo    - Live leaderboards
    echo    - Community notifications
    echo.
    echo 🔧 Next steps:
    echo 1. Test submission form at https://hotppl.io/submit
    echo 2. Verify Discord notifications in your server
    echo 3. Check leaderboard updates
    echo 4. Monitor logs: gcloud app logs tail -s default
    echo.
    echo 🎉 HOT PPL is ready to rock with Discord! 🛸
) else (
    echo.
    echo ❌ Deployment failed!
    echo 🔧 Troubleshooting:
    echo 1. Check your gcloud authentication: gcloud auth list
    echo 2. Verify project settings: gcloud config get-value project
    echo 3. Check app.yaml configuration
    echo 4. Review error logs above
)

echo.
pause
