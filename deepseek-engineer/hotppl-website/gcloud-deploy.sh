#!/bin/bash

# Alternative deployment using Google Cloud App Engine
# For users who prefer gcloud CLI over Firebase

echo "🐋 Deploying HOT PPL Website using Google Cloud App Engine..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI not found. Please install it first:"
    echo "https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔐 Please login to Google Cloud..."
    gcloud auth login
fi

# Set project (replace with your project ID)
PROJECT_ID="hotppl-website"
echo "📋 Setting project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Create app.yaml for App Engine
cat > app.yaml << EOF
runtime: python39

handlers:
# Serve static files
- url: /assets
  static_dir: public/assets
  secure: always

- url: /(.+\.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot))$
  static_files: public/\1
  upload: public/(.+\.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot))$
  secure: always

# Serve HTML pages
- url: /scenes
  static_files: public/scenes.html
  upload: public/scenes.html
  secure: always

- url: /create
  static_files: public/create.html
  upload: public/create.html
  secure: always

- url: /submit
  static_files: public/submit.html
  upload: public/submit.html
  secure: always

- url: /confirmation
  static_files: public/confirmation.html
  upload: public/confirmation.html
  secure: always

# Serve index.html for all other routes
- url: /.*
  static_files: public/index.html
  upload: public/index.html
  secure: always

# Security headers
- url: /.*
  script: auto
  secure: always
  redirect_http_response_code: 301
EOF

# Create main.py (required for App Engine)
cat > main.py << EOF
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Static files served by App Engine'

if __name__ == '__main__':
    app.run(debug=True)
EOF

# Create requirements.txt
cat > requirements.txt << EOF
Flask==2.3.3
EOF

# Deploy to App Engine
echo "🚀 Deploying to Google App Engine..."
gcloud app deploy --quiet

# Get the deployed URL
APP_URL=$(gcloud app describe --format="value(defaultHostname)")
echo "✅ Deployment complete!"
echo "🔗 Your site is live at: https://$APP_URL"

# Set up custom domain
echo ""
echo "🌐 To set up custom domain hotppl.io:"
echo "1. Go to Google Cloud Console > App Engine > Settings > Custom Domains"
echo "2. Click 'Add a custom domain'"
echo "3. Enter 'hotppl.io'"
echo "4. Follow DNS verification steps"
echo "5. Add these DNS records:"
echo "   - A record: @ -> [IP provided by Google]"
echo "   - CNAME: www -> ghs.googlehosted.com"

# Clean up temporary files
rm -f app.yaml main.py requirements.txt

echo ""
echo "🎉 HOT PPL is now live on Google Cloud!"
