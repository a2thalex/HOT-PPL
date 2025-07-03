#!/bin/bash
# HOT PPL Discord REST API CLI
# Lightweight CLI using curl and Discord REST API

# Configuration
DISCORD_BOT_TOKEN="${DISCORD_BOT_TOKEN}"
DISCORD_GUILD_ID="${DISCORD_GUILD_ID}"
DISCORD_API_BASE="https://discord.com/api/v10"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Check if required environment variables are set
check_config() {
    if [[ -z "$DISCORD_BOT_TOKEN" ]]; then
        echo -e "${RED}❌ DISCORD_BOT_TOKEN environment variable not set${NC}"
        exit 1
    fi
    
    if [[ -z "$DISCORD_GUILD_ID" ]]; then
        echo -e "${RED}❌ DISCORD_GUILD_ID environment variable not set${NC}"
        exit 1
    fi
}

# Make authenticated Discord API request
discord_api() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    local url="${DISCORD_API_BASE}${endpoint}"
    local headers=(
        -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"
        -H "Content-Type: application/json"
    )
    
    if [[ -n "$data" ]]; then
        curl -s -X "$method" "${headers[@]}" -d "$data" "$url"
    else
        curl -s -X "$method" "${headers[@]}" "$url"
    fi
}

# Get guild information
get_guild_info() {
    echo -e "${BLUE}📊 Getting guild information...${NC}"
    
    response=$(discord_api "GET" "/guilds/${DISCORD_GUILD_ID}?with_counts=true")
    
    if [[ $? -eq 0 ]]; then
        name=$(echo "$response" | jq -r '.name // "Unknown"')
        member_count=$(echo "$response" | jq -r '.approximate_member_count // 0')
        online_count=$(echo "$response" | jq -r '.approximate_presence_count // 0')
        
        echo -e "${GREEN}✅ Guild: $name${NC}"
        echo -e "${GREEN}👥 Members: $member_count${NC}"
        echo -e "${GREEN}🟢 Online: $online_count${NC}"
    else
        echo -e "${RED}❌ Failed to get guild info${NC}"
    fi
}

# List channels
list_channels() {
    echo -e "${BLUE}📋 Listing channels...${NC}"
    
    response=$(discord_api "GET" "/guilds/${DISCORD_GUILD_ID}/channels")
    
    if [[ $? -eq 0 ]]; then
        echo "$response" | jq -r '.[] | select(.type == 0) | "📝 \(.name) (ID: \(.id))"'
        echo "$response" | jq -r '.[] | select(.type == 2) | "🎤 \(.name) (ID: \(.id))"'
        echo "$response" | jq -r '.[] | select(.type == 4) | "📁 \(.name) (ID: \(.id))"'
    else
        echo -e "${RED}❌ Failed to list channels${NC}"
    fi
}

# Create channel
create_channel() {
    local name="$1"
    local type="${2:-0}"  # 0 = text, 2 = voice, 4 = category
    local topic="$3"
    
    if [[ -z "$name" ]]; then
        echo -e "${RED}❌ Channel name required${NC}"
        return 1
    fi
    
    echo -e "${BLUE}🏗️ Creating channel: $name${NC}"
    
    local data="{\"name\": \"$name\", \"type\": $type"
    if [[ -n "$topic" ]]; then
        data="$data, \"topic\": \"$topic\""
    fi
    data="$data}"
    
    response=$(discord_api "POST" "/guilds/${DISCORD_GUILD_ID}/channels" "$data")
    
    if [[ $? -eq 0 ]]; then
        channel_id=$(echo "$response" | jq -r '.id')
        echo -e "${GREEN}✅ Created channel: $name (ID: $channel_id)${NC}"
    else
        echo -e "${RED}❌ Failed to create channel${NC}"
        echo "$response" | jq -r '.message // "Unknown error"'
    fi
}

# Send message to channel
send_message() {
    local channel_id="$1"
    local message="$2"
    local embed="$3"
    
    if [[ -z "$channel_id" || -z "$message" ]]; then
        echo -e "${RED}❌ Channel ID and message required${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📤 Sending message to channel $channel_id${NC}"
    
    local data="{\"content\": \"$message\""
    if [[ -n "$embed" ]]; then
        data="$data, \"embeds\": [$embed]"
    fi
    data="$data}"
    
    response=$(discord_api "POST" "/channels/${channel_id}/messages" "$data")
    
    if [[ $? -eq 0 ]]; then
        message_id=$(echo "$response" | jq -r '.id')
        echo -e "${GREEN}✅ Message sent (ID: $message_id)${NC}"
    else
        echo -e "${RED}❌ Failed to send message${NC}"
        echo "$response" | jq -r '.message // "Unknown error"'
    fi
}

# Create HOT PPL announcement embed
create_announcement_embed() {
    local title="$1"
    local description="$2"
    local color="16711808"  # Hot pink in decimal
    
    cat <<EOF
{
    "title": "🚨 $title",
    "description": "$description",
    "color": $color,
    "footer": {
        "text": "HOT PPL - Where the f*ck are all the hot people?"
    },
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"
}
EOF
}

# Create submission embed
create_submission_embed() {
    local creator="$1"
    local scene="$2"
    local description="$3"
    local video_url="$4"
    
    local embed="{
        \"title\": \"🎬 New Submission: $scene\",
        \"description\": \"$description\",
        \"color\": 16711808,
        \"fields\": [
            {\"name\": \"👤 Creator\", \"value\": \"$creator\", \"inline\": true},
            {\"name\": \"🎭 Scene\", \"value\": \"$scene\", \"inline\": true}
        ],
        \"footer\": {\"text\": \"React with 🔥 to vote!\"}
    }"
    
    if [[ -n "$video_url" ]]; then
        embed=$(echo "$embed" | jq --arg url "$video_url" '.fields += [{"name": "🎥 Video", "value": "[Watch Here](\($url))", "inline": false}]')
    fi
    
    echo "$embed"
}

# Setup HOT PPL server structure
setup_server() {
    echo -e "${PURPLE}🛸 Setting up HOT PPL Discord server...${NC}"
    
    # Create categories and channels
    declare -A categories=(
        ["📋-INFORMATION"]="Information and announcements"
        ["🎬-CREATION"]="Content creation and submissions"
        ["📊-LIVE-DATA"]="Real-time statistics and leaderboards"
        ["🎉-COMMUNITY"]="Community chat and discussions"
        ["🔒-EXCLUSIVE"]="Exclusive content for top creators"
    )
    
    for category in "${!categories[@]}"; do
        echo -e "${BLUE}Creating category: $category${NC}"
        create_channel "$category" 4 "${categories[$category]}"
        sleep 1  # Rate limiting
    done
    
    # Create specific channels
    declare -A channels=(
        ["📢-announcements"]="Official HOT PPL announcements"
        ["🎬-submissions"]="Submit your scene recreations here"
        ["🗳️-voting"]="Vote on submissions with 🔥 reactions"
        ["🏆-leaderboard"]="Live rankings updated automatically"
        ["💬-general"]="General community chat"
    )
    
    for channel in "${!channels[@]}"; do
        echo -e "${BLUE}Creating channel: $channel${NC}"
        create_channel "$channel" 0 "${channels[$channel]}"
        sleep 1  # Rate limiting
    done
    
    echo -e "${GREEN}✅ Server setup complete!${NC}"
}

# Send announcement
send_announcement() {
    local message="$1"
    local channel_name="${2:-📢-announcements}"
    
    if [[ -z "$message" ]]; then
        echo -e "${RED}❌ Announcement message required${NC}"
        return 1
    fi
    
    # Get channel ID by name
    channels_response=$(discord_api "GET" "/guilds/${DISCORD_GUILD_ID}/channels")
    channel_id=$(echo "$channels_response" | jq -r ".[] | select(.name == \"$channel_name\") | .id")
    
    if [[ -z "$channel_id" || "$channel_id" == "null" ]]; then
        echo -e "${RED}❌ Channel $channel_name not found${NC}"
        return 1
    fi
    
    embed=$(create_announcement_embed "HOT PPL ANNOUNCEMENT" "$message")
    send_message "$channel_id" "" "$embed"
}

# Post submission
post_submission() {
    local creator="$1"
    local scene="$2"
    local description="$3"
    local video_url="$4"
    
    if [[ -z "$creator" || -z "$scene" ]]; then
        echo -e "${RED}❌ Creator and scene required${NC}"
        return 1
    fi
    
    # Get submissions channel ID
    channels_response=$(discord_api "GET" "/guilds/${DISCORD_GUILD_ID}/channels")
    channel_id=$(echo "$channels_response" | jq -r '.[] | select(.name == "🎬-submissions") | .id')
    
    if [[ -z "$channel_id" || "$channel_id" == "null" ]]; then
        echo -e "${RED}❌ Submissions channel not found${NC}"
        return 1
    fi
    
    embed=$(create_submission_embed "$creator" "$scene" "$description" "$video_url")
    send_message "$channel_id" "" "$embed"
}

# Show help
show_help() {
    cat <<EOF
🛸 HOT PPL Discord REST CLI

Usage: $0 [command] [options]

Commands:
  info                          - Show guild information
  channels                      - List all channels
  setup                         - Set up HOT PPL server structure
  announce <message>            - Send announcement
  submit <creator> <scene> [description] [video_url] - Post submission
  create-channel <name> [type] [topic] - Create channel (type: 0=text, 2=voice, 4=category)
  send <channel_id> <message>   - Send message to channel

Environment variables:
  DISCORD_BOT_TOKEN - Your Discord bot token
  DISCORD_GUILD_ID  - Your Discord server ID

Examples:
  $0 info
  $0 setup
  $0 announce "New challenge is live!"
  $0 submit "Minilambobae" "The Arrival" "My take on the arrival scene"
  $0 create-channel "new-channel" 0 "Channel topic"

EOF
}

# Main script logic
main() {
    check_config
    
    case "$1" in
        "info")
            get_guild_info
            ;;
        "channels")
            list_channels
            ;;
        "setup")
            setup_server
            ;;
        "announce")
            send_announcement "$2"
            ;;
        "submit")
            post_submission "$2" "$3" "$4" "$5"
            ;;
        "create-channel")
            create_channel "$2" "$3" "$4"
            ;;
        "send")
            send_message "$2" "$3"
            ;;
        "help"|"--help"|"-h"|"")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Unknown command: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}❌ jq is required but not installed. Please install jq first.${NC}"
    echo "Install with: sudo apt install jq (Ubuntu/Debian) or brew install jq (macOS)"
    exit 1
fi

main "$@"
