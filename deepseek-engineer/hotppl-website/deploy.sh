#!/bin/bash

# HOT PPL Website Deployment Script
# Deploy to hotppl.io using Firebase Hosting

echo "🐋 Deploying HOT PPL Website to hotppl.io..."

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Check if user is logged in
if ! firebase projects:list &> /dev/null; then
    echo "🔐 Please login to Firebase..."
    firebase login
fi

# Initialize Firebase project if needed
if [ ! -f ".firebaserc" ]; then
    echo "🚀 Initializing Firebase project..."
    firebase init hosting
fi

# Build and deploy
echo "📦 Building website..."

# Create placeholder assets if they don't exist
mkdir -p public/assets

# Create placeholder images
if [ ! -f "public/assets/placeholder.jpg" ]; then
    echo "🖼️ Creating placeholder images..."
    # You can replace these with actual images
    touch public/assets/placeholder.jpg
    touch public/assets/video-preview.mp4
    touch public/assets/minilambobae.jpg
    touch public/assets/becca.jpg
    touch public/assets/jenny.jpg
    touch public/assets/scene_arrival.jpg
    touch public/assets/scene_dj.jpg
    touch public/assets/scene_tracksuit.jpg
    touch public/assets/scene_siri.jpg
    touch public/assets/scene_judgment.jpg
    touch public/assets/inspiration1.jpg
    touch public/assets/inspiration2.jpg
    touch public/assets/inspiration3.jpg
    touch public/assets/inspiration4.jpg
fi

# Deploy to Firebase
echo "🚀 Deploying to Firebase Hosting..."
firebase deploy --only hosting

# Set up custom domain (manual step)
echo "🌐 To set up custom domain hotppl.io:"
echo "1. Go to Firebase Console > Hosting"
echo "2. Click 'Add custom domain'"
echo "3. Enter 'hotppl.io'"
echo "4. Follow DNS configuration instructions"
echo "5. Add these DNS records to your domain registrar:"
echo "   - A record: @ -> 151.101.1.195"
echo "   - A record: @ -> 151.101.65.195"
echo "   - CNAME: www -> hotppl-website.web.app"

echo "✅ Deployment complete!"
echo "🔗 Your site is live at: https://hotppl-website.web.app"
echo "🔗 Custom domain will be: https://hotppl.io (after DNS setup)"
