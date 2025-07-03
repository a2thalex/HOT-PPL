# 🚀 HOT PPL Discord Bot - QUICK SETUP

## 🎯 Get Your Discord Bot Running in 5 Minutes!

### Step 1: Create Discord Bot (2 minutes)

1. **Go to Discord Developer Portal**: https://discord.com/developers/applications
2. **Click "New Application"** → Name it "HOT PPL Bot"
3. **Go to "Bot" section** → Click "Add Bot"
4. **Copy the Token** → This is your `DISCORD_BOT_TOKEN`
5. **Enable these permissions**:
   - Send Messages ✅
   - Manage Messages ✅
   - Embed Links ✅
   - Add Reactions ✅
   - Read Message History ✅
   - Use Slash Commands ✅

### Step 2: Get Your Server ID (30 seconds)

1. **Enable Developer Mode** in Discord (User Settings → Advanced → Developer Mode)
2. **Right-click your HOT PPL server** → "Copy ID"
3. **This is your `DISCORD_GUILD_ID`**

### Step 3: Invite Bot to Server (30 seconds)

1. **Go to "OAuth2" → "URL Generator"** in Developer Portal
2. **Select scopes**: `bot` and `applications.commands`
3. **Select permissions**: 
   - Manage Channels
   - Send Messages
   - Manage Messages
   - Embed Links
   - Add Reactions
4. **Copy the URL** → Open it → Select your server → Authorize

### Step 4: Configure Environment (1 minute)

Edit the `.env` file with your values:

```bash
DISCORD_BOT_TOKEN=YOUR_ACTUAL_BOT_TOKEN_HERE
DISCORD_GUILD_ID=YOUR_ACTUAL_GUILD_ID_HERE
DISCORD_CLIENT_ID=YOUR_APPLICATION_ID_HERE
```

### Step 5: Deploy Bot (1 minute)

```bash
# Test connection
python discord-cli.py stats

# Set up server structure
python discord-cli.py setup

# Start the bot
python discord-bot.py
```

## 🔥 Quick Commands

Once running, your bot will handle:

- **Submissions**: Users can submit videos with `!hotppl submit [scene] [description]`
- **Voting**: React with 🔥 to vote on submissions
- **Leaderboard**: `!hotppl leaderboard` shows top submissions
- **Stats**: `!hotppl stats` shows user statistics

## 🚀 Integration with hotppl.io

The bot automatically:
- Posts new submissions from website to Discord
- Syncs votes between Discord and website
- Updates live leaderboards
- Sends notifications for new content

## 🛠️ Troubleshooting

**Bot not responding?**
- Check bot token in .env file
- Make sure bot has permissions in your server
- Verify bot is online (green dot in Discord)

**Can't see channels?**
- Run `python discord-cli.py setup` to create channel structure
- Check bot has "Manage Channels" permission

**Votes not working?**
- Bot needs "Add Reactions" and "Read Message History" permissions
- Make sure voting channel exists

## 🎯 Next Steps

1. **Test the bot** with a few submissions
2. **Invite your community** to start using it
3. **Monitor the leaderboard** for engagement
4. **Add more features** as needed

**Your Discord-powered HOT PPL community is ready to rock! 🛸**
