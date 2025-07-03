# 🚀 HOT PPL Website Deployment Guide

Complete guide to deploy the HOT PPL website to **hotppl.io** using Google Cloud.

## 🎯 Deployment Options

### Option 1: Firebase Hosting (Recommended)
**Best for:** Static websites, easy setup, automatic SSL
```bash
# Windows
deploy.bat

# Linux/Mac  
./deploy.sh
```

### Option 2: Google App Engine
**Best for:** More control, custom backends, enterprise features
```bash
./gcloud-deploy.sh
```

### Option 3: Manual Firebase Setup
**Best for:** Custom configuration, learning purposes
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

## 📋 Prerequisites Checklist

- [ ] **Node.js 18+** installed
- [ ] **Google Cloud account** with billing enabled
- [ ] **Domain ownership** of hotppl.io
- [ ] **Firebase CLI** or **gcloud CLI** installed
- [ ] **Project assets** (images, videos) ready

## 🏗️ Project Structure Created

```
hotppl-website/
├── 📁 public/
│   ├── 🏠 index.html          # Landing page
│   ├── 🎬 scenes.html         # Scene selection  
│   ├── 🎨 create.html         # Creation tools (needs completion)
│   ├── 📤 submit.html         # Submission form (needs completion)
│   ├── ✅ confirmation.html   # Success page (needs completion)
│   └── 📁 assets/             # Media files (needs actual content)
├── ⚙️ firebase.json           # Firebase configuration
├── 🔧 .firebaserc            # Project settings
├── 📦 package.json           # NPM configuration
├── 🚀 deploy.sh              # Auto-deployment (Linux/Mac)
├── 🚀 deploy.bat             # Auto-deployment (Windows)
├── ☁️ gcloud-deploy.sh       # App Engine deployment
└── 📖 README.md              # Documentation
```

## 🎨 Assets Needed

Replace these placeholder files with actual content:

### 🖼️ Images Required
```
public/assets/
├── placeholder.jpg           # Video thumbnail
├── minilambobae.jpg         # Character: Lead Alien
├── becca.jpg                # Character: Tech Expert  
├── jenny.jpg                # Character: Fashionista
├── scene_arrival.jpg        # Scene: The Arrival
├── scene_dj.jpg             # Scene: DJ Reveal
├── scene_tracksuit.jpg      # Scene: Tracksuit Encounter
├── scene_siri.jpg           # Scene: Siri Consultation
├── scene_judgment.jpg       # Scene: Final Judgment
├── inspiration1.jpg         # Gallery inspiration
├── inspiration2.jpg         # Gallery inspiration
├── inspiration3.jpg         # Gallery inspiration
└── inspiration4.jpg         # Gallery inspiration
```

### 🎥 Video Required
```
public/assets/
└── video-preview.mp4        # Main music video preview
```

## 🌐 Domain Setup: hotppl.io

### Step 1: Deploy to Firebase/App Engine
First deploy to get the hosting URL:
- Firebase: `https://hotppl-website.web.app`
- App Engine: `https://hotppl-website.uc.r.appspot.com`

### Step 2: Add Custom Domain
**Firebase Console:**
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select project → Hosting → Add custom domain
3. Enter `hotppl.io` and `www.hotppl.io`

**App Engine Console:**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. App Engine → Settings → Custom domains
3. Add domain and verify ownership

### Step 3: DNS Configuration
Add these records to your domain registrar:

**For Firebase Hosting:**
```dns
Type: A     | Name: @   | Value: 151.101.1.195
Type: A     | Name: @   | Value: 151.101.65.195  
Type: CNAME | Name: www | Value: hotppl-website.web.app
```

**For App Engine:**
```dns
Type: A     | Name: @   | Value: [IP from Google]
Type: CNAME | Name: www | Value: ghs.googlehosted.com
```

## ⚡ Quick Deploy Commands

### Firebase (Recommended)
```bash
# Install dependencies
npm install -g firebase-tools

# Login and deploy
firebase login
firebase init hosting
firebase deploy --only hosting

# Custom domain
firebase hosting:sites:create hotppl-website
```

### App Engine Alternative  
```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Login and deploy
gcloud auth login
gcloud config set project hotppl-website
gcloud app deploy
```

## 🔧 Configuration Features

### ✅ Included Features
- **Responsive Design** - Mobile-first approach
- **SEO Optimization** - Meta tags, structured data
- **Performance** - Optimized loading, CDN
- **Security** - HTTPS, content security policy
- **Age Verification** - 18+ gate with localStorage
- **Progress Tracking** - Session storage for user flow
- **Clean URLs** - SEO-friendly routing

### 🎛️ Firebase Configuration
```json
{
  "hosting": {
    "public": "public",
    "cleanUrls": true,
    "trailingSlash": false,
    "rewrites": [
      {"source": "/scenes", "destination": "/scenes.html"},
      {"source": "/create", "destination": "/create.html"},
      {"source": "/submit", "destination": "/submit.html"},
      {"source": "/confirmation", "destination": "/confirmation.html"}
    ]
  }
}
```

## 📊 Monitoring & Analytics

### Google Analytics Setup
Add to each HTML page:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Performance Monitoring
```bash
firebase init performance
firebase deploy --only hosting,functions
```

## 💰 Cost Estimation

### Firebase Hosting
- **Free Tier**: 10GB storage, 10GB/month transfer
- **Typical Cost**: $5-50/month depending on traffic
- **Custom Domain**: Free SSL certificate included

### App Engine
- **Free Tier**: 28 instance hours/day
- **Typical Cost**: $10-100/month depending on usage
- **Custom Domain**: Free SSL certificate included

## 🚨 Content Compliance

### Age Verification
- 18+ age gate implemented
- localStorage verification
- Redirect to Google if declined

### Content Warnings
- Adult content disclaimers
- Explicit language warnings
- Platform policy compliance

## 🆘 Troubleshooting

### Common Issues
1. **Domain not working**: Check DNS propagation (24-48 hours)
2. **Deploy fails**: Update Firebase CLI, re-login
3. **Assets not loading**: Verify file paths, check permissions
4. **Age gate not working**: Clear localStorage, check JavaScript

### Support Resources
- [Firebase Documentation](https://firebase.google.com/docs/hosting)
- [Google Cloud Documentation](https://cloud.google.com/appengine/docs)
- [HOT PPL Discord](https://discord.gg/hotppl)

## ✅ Deployment Checklist

- [ ] Install Firebase CLI or gcloud CLI
- [ ] Login to Google Cloud account
- [ ] Create/select project
- [ ] Add actual images and video to assets/
- [ ] Run deployment script
- [ ] Verify site loads correctly
- [ ] Set up custom domain hotppl.io
- [ ] Configure DNS records
- [ ] Test age verification
- [ ] Set up analytics
- [ ] Test all page navigation
- [ ] Verify mobile responsiveness

## 🎉 Go Live!

Once everything is set up:

1. **Run deployment**: `./deploy.sh` or `deploy.bat`
2. **Verify deployment**: Check the provided URL
3. **Set up domain**: Follow DNS instructions
4. **Test thoroughly**: All pages and features
5. **Monitor**: Set up analytics and monitoring

**🔥 Your HOT PPL website will be live at https://hotppl.io!**

---

Need help? Join the [HOT PPL Discord](https://discord.gg/hotppl) or email dev@hotppl.com
