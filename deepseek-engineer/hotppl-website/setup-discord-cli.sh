#!/bin/bash
# HOT PPL Discord CLI Setup Script
# Installs and configures Discord CLI tools

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}🛸 HOT PPL Discord CLI Setup${NC}"
echo "Setting up Discord CLI tools for HOT PPL platform..."

# Check if running on supported OS
check_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
    else
        echo -e "${RED}❌ Unsupported OS: $OSTYPE${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Detected OS: $OS${NC}"
}

# Install dependencies
install_dependencies() {
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    
    case $OS in
        "linux")
            # Update package list
            sudo apt update
            
            # Install required packages
            sudo apt install -y python3 python3-pip nodejs npm jq curl git
            
            # Install Python packages
            pip3 install discord.py requests aiohttp python-dotenv
            ;;
        "macos")
            # Check if Homebrew is installed
            if ! command -v brew &> /dev/null; then
                echo -e "${YELLOW}Installing Homebrew...${NC}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            
            # Install packages
            brew install python3 node jq curl git
            
            # Install Python packages
            pip3 install discord.py requests aiohttp python-dotenv
            ;;
        "windows")
            echo -e "${YELLOW}⚠️ Windows detected. Please install manually:${NC}"
            echo "1. Python 3.8+: https://python.org/downloads/"
            echo "2. Node.js: https://nodejs.org/"
            echo "3. Git: https://git-scm.com/"
            echo "4. Run: pip install discord.py requests aiohttp python-dotenv"
            read -p "Press Enter when dependencies are installed..."
            ;;
    esac
    
    echo -e "${GREEN}✅ Dependencies installed${NC}"
}

# Install Discord CLI tools
install_discord_tools() {
    echo -e "${BLUE}🤖 Installing Discord CLI tools...${NC}"
    
    # Make our CLI scripts executable
    chmod +x discord-cli.py
    chmod +x discord-rest-cli.sh
    
    # Install discord-cli-tools (third-party)
    if command -v npm &> /dev/null; then
        echo -e "${BLUE}Installing discord-cli-tools...${NC}"
        npm install -g discord-cli-tools 2>/dev/null || echo -e "${YELLOW}⚠️ discord-cli-tools installation failed (optional)${NC}"
    fi
    
    # Install discordcli (Go-based tool)
    if command -v go &> /dev/null; then
        echo -e "${BLUE}Installing discordcli...${NC}"
        go install github.com/diamondburned/discordcli@latest 2>/dev/null || echo -e "${YELLOW}⚠️ discordcli installation failed (optional)${NC}"
    fi
    
    echo -e "${GREEN}✅ Discord CLI tools installed${NC}"
}

# Create environment file
create_env_file() {
    echo -e "${BLUE}⚙️ Creating environment configuration...${NC}"
    
    if [[ ! -f .env ]]; then
        cat > .env << 'EOF'
# HOT PPL Discord Configuration
# Get these values from Discord Developer Portal

# Discord Bot Token (from Bot section)
DISCORD_BOT_TOKEN=your_bot_token_here

# Discord Server (Guild) ID
DISCORD_GUILD_ID=your_guild_id_here

# Discord OAuth2 (from OAuth2 section)
DISCORD_CLIENT_ID=your_client_id_here
DISCORD_CLIENT_SECRET=your_client_secret_here
DISCORD_REDIRECT_URI=https://hotppl.io/auth/discord

# Discord Webhook URL (for notifications)
DISCORD_WEBHOOK_URL=your_webhook_url_here

# Flask configuration
FLASK_SECRET_KEY=your_flask_secret_key_here
EOF
        echo -e "${GREEN}✅ Created .env file${NC}"
        echo -e "${YELLOW}⚠️ Please edit .env file with your Discord credentials${NC}"
    else
        echo -e "${YELLOW}⚠️ .env file already exists${NC}"
    fi
}

# Create Discord bot setup guide
create_bot_guide() {
    cat > DISCORD-BOT-SETUP.md << 'EOF'
# 🤖 Discord Bot Setup Guide

## Step 1: Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name it "HOT PPL Bot"
4. Save the **Application ID** (this is your CLIENT_ID)

## Step 2: Create Bot

1. Go to "Bot" section in your application
2. Click "Add Bot"
3. Copy the **Token** (this is your BOT_TOKEN)
4. Enable these permissions:
   - Send Messages
   - Manage Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Add Reactions
   - Use Slash Commands

## Step 3: Get Server ID

1. Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
2. Right-click your server name
3. Click "Copy ID" (this is your GUILD_ID)

## Step 4: Invite Bot to Server

1. Go to "OAuth2" > "URL Generator" in Developer Portal
2. Select scopes: `bot` and `applications.commands`
3. Select permissions:
   - Manage Channels
   - Send Messages
   - Manage Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Add Reactions
   - Use Slash Commands
4. Copy the generated URL and open it
5. Select your server and authorize

## Step 5: Create Webhook (Optional)

1. Go to your Discord server
2. Right-click a channel > Edit Channel > Integrations > Webhooks
3. Click "New Webhook"
4. Copy the webhook URL

## Step 6: Update .env File

Edit the `.env` file with your values:

```bash
DISCORD_BOT_TOKEN=your_actual_bot_token
DISCORD_GUILD_ID=your_actual_guild_id
DISCORD_CLIENT_ID=your_actual_client_id
DISCORD_CLIENT_SECRET=your_actual_client_secret
DISCORD_WEBHOOK_URL=your_actual_webhook_url
```

## Step 7: Test the Bot

```bash
# Test basic connection
python3 discord-cli.py stats

# Set up server structure
python3 discord-cli.py setup

# Send test announcement
python3 discord-cli.py announce --message "HOT PPL bot is online! 🛸"
```

## Troubleshooting

- **403 Forbidden**: Bot doesn't have required permissions
- **404 Not Found**: Guild ID is incorrect or bot isn't in server
- **401 Unauthorized**: Bot token is incorrect
- **Rate Limited**: Too many requests, wait and try again

EOF
    echo -e "${GREEN}✅ Created Discord bot setup guide${NC}"
}

# Create CLI aliases
create_aliases() {
    echo -e "${BLUE}🔗 Creating CLI aliases...${NC}"
    
    cat > discord-aliases.sh << 'EOF'
#!/bin/bash
# HOT PPL Discord CLI Aliases

# Load environment variables
if [[ -f .env ]]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Python CLI aliases
alias hotppl-setup='python3 discord-cli.py setup'
alias hotppl-stats='python3 discord-cli.py stats'
alias hotppl-announce='python3 discord-cli.py announce'
alias hotppl-submit='python3 discord-cli.py submit'
alias hotppl-leaderboard='python3 discord-cli.py leaderboard'

# REST CLI aliases
alias hotppl-info='./discord-rest-cli.sh info'
alias hotppl-channels='./discord-rest-cli.sh channels'
alias hotppl-rest-setup='./discord-rest-cli.sh setup'

# Quick commands
alias hotppl-bot-start='python3 discord-bot.py'
alias hotppl-api-start='python3 discord-api.py'

echo "🛸 HOT PPL Discord CLI aliases loaded!"
echo "Available commands:"
echo "  hotppl-setup      - Set up Discord server"
echo "  hotppl-stats      - Show server statistics"
echo "  hotppl-announce   - Send announcement"
echo "  hotppl-submit     - Submit new content"
echo "  hotppl-leaderboard - Update leaderboard"
echo "  hotppl-bot-start  - Start Discord bot"
echo "  hotppl-api-start  - Start API server"
EOF
    
    chmod +x discord-aliases.sh
    echo -e "${GREEN}✅ Created CLI aliases${NC}"
    echo -e "${YELLOW}💡 Run 'source discord-aliases.sh' to load aliases${NC}"
}

# Create systemd service (Linux only)
create_systemd_service() {
    if [[ "$OS" == "linux" ]]; then
        echo -e "${BLUE}🔧 Creating systemd service...${NC}"
        
        cat > hotppl-discord-bot.service << EOF
[Unit]
Description=HOT PPL Discord Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=/usr/bin:/usr/local/bin
EnvironmentFile=$(pwd)/.env
ExecStart=/usr/bin/python3 $(pwd)/discord-bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        
        echo -e "${GREEN}✅ Created systemd service file${NC}"
        echo -e "${YELLOW}💡 To install: sudo cp hotppl-discord-bot.service /etc/systemd/system/${NC}"
        echo -e "${YELLOW}💡 To enable: sudo systemctl enable hotppl-discord-bot${NC}"
        echo -e "${YELLOW}💡 To start: sudo systemctl start hotppl-discord-bot${NC}"
    fi
}

# Main setup function
main() {
    echo -e "${PURPLE}Starting HOT PPL Discord CLI setup...${NC}"
    
    check_os
    install_dependencies
    install_discord_tools
    create_env_file
    create_bot_guide
    create_aliases
    create_systemd_service
    
    echo -e "${GREEN}🎉 Setup complete!${NC}"
    echo
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Read DISCORD-BOT-SETUP.md for Discord configuration"
    echo "2. Edit .env file with your Discord credentials"
    echo "3. Run: source discord-aliases.sh"
    echo "4. Test with: hotppl-stats"
    echo
    echo -e "${PURPLE}🛸 HOT PPL Discord CLI is ready to rock!${NC}"
}

# Run main function
main "$@"
