@echo off
REM HOT PPL Domain Setup Script
REM Configure hotppl.io to point to Firebase Hosting

echo 🌐 Setting up hotppl.io domain for HOT PPL...
echo.

echo 📋 Firebase Hosting Setup Complete!
echo ✅ Your website is live at: https://hot-ppl.web.app
echo.

echo 🔧 To connect hotppl.io domain:
echo.
echo 1. Go to Firebase Console: https://console.firebase.google.com/project/hot-ppl/hosting
echo 2. Click "Add custom domain"
echo 3. Enter "hotppl.io"
echo 4. Follow the verification steps
echo.

echo 📝 DNS Records needed for hotppl.io:
echo.
echo For Firebase Hosting, add these DNS records:
echo.
echo A Records:
echo   Type: A
echo   Name: @
echo   Value: 151.101.1.195
echo   TTL: 3600
echo.
echo   Type: A  
echo   Name: @
echo   Value: 151.101.65.195
echo   TTL: 3600
echo.
echo CNAME Record:
echo   Type: CNAME
echo   Name: www
echo   Value: hot-ppl.web.app
echo   TTL: 3600
echo.

echo 🚀 Alternative: Use Namecheap CLI (if configured)
echo.
echo If you have Namecheap CLI set up, you can run:
echo   namecheap-cli dns set hotppl.io A @ 151.101.1.195
echo   namecheap-cli dns set hotppl.io A @ 151.101.65.195  
echo   namecheap-cli dns set hotppl.io CNAME www hot-ppl.web.app
echo.

echo ⏰ DNS propagation takes 24-48 hours
echo 🔍 Check status: https://dnschecker.org/#A/hotppl.io
echo.

echo 🎉 Once DNS propagates, hotppl.io will show your HOT PPL website!
echo.

REM Open Firebase Console
echo 🌐 Opening Firebase Console...
start https://console.firebase.google.com/project/hot-ppl/hosting

REM Open the live website
echo 🚀 Opening your live website...
start https://hot-ppl.web.app

echo.
echo ✅ Deployment complete! Your HOT PPL website is live!
echo 🔗 Current URL: https://hot-ppl.web.app
echo 🔗 Future URL: https://hotppl.io (after DNS setup)
echo.

pause
