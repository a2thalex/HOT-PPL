# 🪝 Discord Webhook Setup for HOT PPL

## Quick Setup (2 minutes)

### Step 1: Create Webhook in Discord

1. **Go to your HOT PPL Discord server**
2. **Right-click on the `#🎬-submissions` channel**
3. **Select "Edit Channel"**
4. **Go to "Integrations" tab**
5. **Click "Create Webhook"**
6. **Name it**: `HOT PPL Submissions`
7. **Copy the Webhook URL** (looks like: `https://discord.com/api/webhooks/...`)

### Step 2: Add Webhook URL to Environment

**Option A: Update .env file**
```bash
# Add this line to your .env file
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL_HERE
```

**Option B: Update app.yaml for Google Cloud**
```yaml
env_variables:
  # ... other variables ...
  DISCORD_WEBHOOK_URL: "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL_HERE"
```

### Step 3: Test the Integration

Run the test script:
```bash
python test_webhook.py
```

## What This Enables

✅ **Automatic submission posting** - New submissions from hotppl.io automatically appear in Discord  
✅ **Rich embeds** - Beautiful formatted messages with submission details  
✅ **Real-time notifications** - Community gets notified instantly  
✅ **Easy voting** - React with 🔥 to vote on submissions  

## Webhook vs Bot

**Webhook (Recommended for App Engine):**
- ✅ Simple to set up
- ✅ Works great with serverless
- ✅ No persistent connection needed
- ✅ Perfect for posting messages

**Full Bot (For advanced features):**
- 🔄 Real-time voting sync
- 🔄 Command handling
- 🔄 Advanced moderation
- ❌ Requires persistent connection

## Troubleshooting

**Webhook not working?**
1. Check the webhook URL is correct
2. Make sure the channel still exists
3. Verify webhook hasn't been deleted
4. Test with a simple curl command:

```bash
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content": "Test message from HOT PPL!"}'
```

**Still having issues?**
- Check Discord server permissions
- Verify the webhook URL format
- Look at Google Cloud logs: `gcloud app logs tail -s default`

## Security Notes

🔒 **Keep your webhook URL secret!** Anyone with the URL can post to your channel.  
🔒 **Don't commit webhook URLs to public repositories**  
🔒 **Use environment variables for production**  

## Next Steps

Once webhook is set up:
1. Deploy to Google Cloud: `./deploy_with_discord.bat`
2. Test submissions at: https://hotppl.io/submit
3. Watch Discord for automatic posts!
4. Monitor with: `gcloud app logs tail -s default`

🎉 **Your Discord-integrated HOT PPL platform is ready!** 🛸
