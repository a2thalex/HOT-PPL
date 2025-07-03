@echo off
REM HOT PPL Website Deployment Script for Windows
REM Deploy to hotppl.io using Firebase Hosting

echo 🐋 Deploying HOT PPL Website to hotppl.io...

REM Check if Firebase CLI is installed
firebase --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Firebase CLI not found. Installing...
    npm install -g firebase-tools
)

REM Check if user is logged in
firebase projects:list >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔐 Please login to Firebase...
    firebase login
)

REM Initialize Firebase project if needed
if not exist ".firebaserc" (
    echo 🚀 Initializing Firebase project...
    firebase init hosting
)

REM Build and deploy
echo 📦 Building website...

REM Create placeholder assets if they don't exist
if not exist "public\assets" mkdir public\assets

REM Create placeholder images (you can replace these with actual images)
if not exist "public\assets\placeholder.jpg" (
    echo 🖼️ Creating placeholder images...
    echo. > public\assets\placeholder.jpg
    echo. > public\assets\video-preview.mp4
    echo. > public\assets\minilambobae.jpg
    echo. > public\assets\becca.jpg
    echo. > public\assets\jenny.jpg
    echo. > public\assets\scene_arrival.jpg
    echo. > public\assets\scene_dj.jpg
    echo. > public\assets\scene_tracksuit.jpg
    echo. > public\assets\scene_siri.jpg
    echo. > public\assets\scene_judgment.jpg
    echo. > public\assets\inspiration1.jpg
    echo. > public\assets\inspiration2.jpg
    echo. > public\assets\inspiration3.jpg
    echo. > public\assets\inspiration4.jpg
)

REM Deploy to Firebase
echo 🚀 Deploying to Firebase Hosting...
firebase deploy --only hosting

REM Set up custom domain (manual step)
echo.
echo 🌐 To set up custom domain hotppl.io:
echo 1. Go to Firebase Console ^> Hosting
echo 2. Click 'Add custom domain'
echo 3. Enter 'hotppl.io'
echo 4. Follow DNS configuration instructions
echo 5. Add these DNS records to your domain registrar:
echo    - A record: @ -^> 151.101.1.195
echo    - A record: @ -^> 151.101.65.195
echo    - CNAME: www -^> hotppl-website.web.app
echo.
echo ✅ Deployment complete!
echo 🔗 Your site is live at: https://hotppl-website.web.app
echo 🔗 Custom domain will be: https://hotppl.io (after DNS setup)

pause
