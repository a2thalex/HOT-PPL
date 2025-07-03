# 🐋 HOT PPL Website Deployment

Deploy the HOT PPL website to **hotppl.io** using Google Cloud Firebase Hosting.

## 🚀 Quick Deploy

### Prerequisites
- [Node.js](https://nodejs.org/) installed
- [Firebase CLI](https://firebase.google.com/docs/cli) installed
- Google Cloud account with billing enabled
- Domain ownership of `hotppl.io`

### One-Click Deploy

**Windows:**
```bash
deploy.bat
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

## 📁 Project Structure

```
hotppl-website/
├── public/                 # Static website files
│   ├── index.html         # Landing page
│   ├── scenes.html        # Scene selection
│   ├── create.html        # Creation tools (to be added)
│   ├── submit.html        # Submission form (to be added)
│   ├── confirmation.html  # Success page (to be added)
│   └── assets/            # Images, videos, media
├── firebase.json          # Firebase hosting config
├── .firebaserc           # Firebase project config
├── deploy.sh             # Linux/Mac deployment script
├── deploy.bat            # Windows deployment script
└── README.md             # This file
```

## 🛠️ Manual Setup

### 1. Install Firebase CLI
```bash
npm install -g firebase-tools
```

### 2. Login to Firebase
```bash
firebase login
```

### 3. Initialize Project
```bash
firebase init hosting
```

Select:
- Use existing project or create new one
- Public directory: `public`
- Single-page app: `No`
- Automatic builds: `No`

### 4. Deploy
```bash
firebase deploy --only hosting
```

## 🌐 Custom Domain Setup (hotppl.io)

### 1. Firebase Console Setup
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project
3. Go to **Hosting** section
4. Click **Add custom domain**
5. Enter `hotppl.io`
6. Follow verification steps

### 2. DNS Configuration
Add these records to your domain registrar (where you bought hotppl.io):

**A Records:**
```
Type: A
Name: @
Value: 151.101.1.195
TTL: 3600

Type: A  
Name: @
Value: 151.101.65.195
TTL: 3600
```

**CNAME Record:**
```
Type: CNAME
Name: www
Value: hotppl-website.web.app
TTL: 3600
```

### 3. SSL Certificate
Firebase automatically provisions SSL certificates for custom domains.

## 📊 Website Features

### Current Pages
- **Landing Page** (`/`) - Main entry with video preview
- **Scene Selection** (`/scenes`) - Choose scenes to recreate
- **Create Guide** (`/create`) - Tools and instructions
- **Submit Form** (`/submit`) - Upload and submission
- **Confirmation** (`/confirmation`) - Success page

### Technical Features
- **Responsive Design** - Mobile-first approach
- **Progressive Web App** ready
- **SEO Optimized** - Meta tags and structure
- **Fast Loading** - Optimized assets and CDN
- **Age Gate** - 18+ verification
- **Session Storage** - User progress tracking

## 🎨 Assets Needed

Replace placeholder files in `public/assets/` with actual content:

### Images
- `placeholder.jpg` - Video thumbnail
- `minilambobae.jpg` - Character photo
- `becca.jpg` - Character photo  
- `jenny.jpg` - Character photo
- `scene_*.jpg` - Scene thumbnails (5 files)
- `inspiration*.jpg` - Gallery images (4 files)

### Video
- `video-preview.mp4` - Main preview video

## 🔧 Configuration

### Firebase Hosting Config (`firebase.json`)
- Clean URLs enabled
- Custom redirects for SEO-friendly URLs
- Cache headers for performance
- Compression enabled

### Security Headers
- Content Security Policy
- X-Frame-Options
- X-Content-Type-Options

## 📈 Analytics & Monitoring

### Google Analytics (Recommended)
Add to `<head>` of each page:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Firebase Performance Monitoring
```bash
firebase init performance
```

## 🚨 Content Warnings

This website contains:
- Adult content (18+ only)
- Explicit language
- Age verification required

Ensure compliance with:
- Local content regulations
- Platform policies
- Age verification laws

## 🔄 Updates & Maintenance

### Deploy Updates
```bash
firebase deploy --only hosting
```

### Rollback
```bash
firebase hosting:clone SOURCE_SITE_ID:SOURCE_VERSION_ID TARGET_SITE_ID
```

### View Logs
```bash
firebase functions:log
```

## 💰 Costs

### Firebase Hosting
- **Free Tier**: 10GB storage, 10GB/month transfer
- **Paid**: $0.026/GB storage, $0.15/GB transfer
- **Custom Domain**: Free SSL certificate

### Estimated Monthly Cost
- Small site (< 10GB): **Free**
- Medium traffic: **$5-20/month**
- High traffic: **$50-200/month**

## 🆘 Troubleshooting

### Common Issues

**Domain not working:**
- Check DNS propagation (24-48 hours)
- Verify DNS records are correct
- Clear browser cache

**Deploy fails:**
- Check Firebase CLI version: `firebase --version`
- Re-login: `firebase logout && firebase login`
- Check project permissions

**Assets not loading:**
- Verify file paths in HTML
- Check file permissions
- Clear CDN cache

### Support
- [Firebase Documentation](https://firebase.google.com/docs/hosting)
- [Firebase Support](https://firebase.google.com/support)
- [Community Forum](https://stackoverflow.com/questions/tagged/firebase-hosting)

## 📞 Contact

For deployment issues or questions:
- **Email**: dev@hotppl.com
- **Discord**: [HOT PPL Community](https://discord.gg/hotppl)

---

**🔥 Ready to deploy? Run the deployment script and get HOT PPL live on hotppl.io!**
