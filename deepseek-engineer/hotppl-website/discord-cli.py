#!/usr/bin/env python3
"""
HOT PPL Discord CLI - Command-line interface for Discord management
Usage: python discord-cli.py [command] [options]
"""

import discord
import asyncio
import argparse
import json
import os
import sys
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', '0'))

# Validate configuration
if not DISCORD_BOT_TOKEN:
    print("❌ DISCORD_BOT_TOKEN not found in environment variables")
    print("Please check your .env file")
    sys.exit(1)

if DISCORD_GUILD_ID == 0:
    print("❌ DISCORD_GUILD_ID not found in environment variables")
    print("Please check your .env file")
    sys.exit(1)

class DiscordCLI:
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        # Don't require privileged intents for now
        
        self.client = discord.Client(intents=intents)
        self.guild = None
        
    async def connect(self):
        """Connect to Discord"""
        await self.client.login(DISCORD_BOT_TOKEN)
        await self.client.connect()
        
        # Get guild
        self.guild = self.client.get_guild(DISCORD_GUILD_ID)
        if not self.guild:
            print(f"❌ Could not find guild with ID {DISCORD_GUILD_ID}")
            return False
        
        print(f"✅ Connected to {self.guild.name}")
        return True
    
    async def setup_server(self):
        """Set up HOT PPL Discord server structure"""
        print("🏗️ Setting up HOT PPL Discord server...")
        
        # Create categories
        categories = {
            "📋 INFORMATION": [
                ("📢-announcements", "Official HOT PPL announcements"),
                ("📖-rules", "Server rules and guidelines"),
                ("🎯-current-challenge", "Current music video challenge"),
                ("🏆-hall-of-fame", "Best submissions of all time")
            ],
            "🎬 CREATION": [
                ("🎬-submissions", "Submit your scene recreations"),
                ("🗳️-voting", "Vote on submissions with 🔥 reactions"),
                ("💬-feedback", "Detailed feedback and discussions"),
                ("🤝-collaborations", "Find collaboration partners")
            ],
            "📊 LIVE DATA": [
                ("🏆-leaderboard", "Live rankings (auto-updated)"),
                ("📈-stats", "Community statistics"),
                ("🔥-trending", "Trending submissions")
            ],
            "🎉 COMMUNITY": [
                ("💬-general", "General community chat"),
                ("🎨-inspiration", "Share ideas and inspiration"),
                ("🛠️-tools-and-tips", "Creator resources and tips"),
                ("🎤-voice-hangout", "Voice chat channel")
            ],
            "🔒 EXCLUSIVE": [
                ("👑-vip-creators", "Top 10 creators only"),
                ("🎭-behind-scenes", "Creator insights and process"),
                ("🚀-early-access", "New features and challenges first")
            ]
        }
        
        for category_name, channels in categories.items():
            # Create category
            category = await self.guild.create_category(category_name)
            print(f"📁 Created category: {category_name}")
            
            for channel_name, topic in channels:
                if channel_name == "🎤-voice-hangout":
                    # Create voice channel
                    await self.guild.create_voice_channel(
                        channel_name,
                        category=category
                    )
                else:
                    # Create text channel
                    await self.guild.create_text_channel(
                        channel_name,
                        category=category,
                        topic=topic
                    )
                print(f"  📝 Created channel: {channel_name}")
        
        print("✅ Server setup complete!")
    
    async def create_roles(self):
        """Create HOT PPL roles"""
        print("👑 Creating roles...")
        
        roles = [
            ("🛸 Alien Admin", 0xff0080, True),  # Hot pink, hoisted
            ("🎬 Top Creator", 0x00ff88, True),   # Neon green, hoisted
            ("✅ Verified Creator", 0x00d4ff, False), # Neon blue
            ("🤝 Community Helper", 0x8000ff, False), # Purple
            ("🎭 Scene Master", 0xff4000, False),  # Orange
            ("👽 Earthling", 0x666666, False)     # Gray (default)
        ]
        
        for name, color, hoist in roles:
            try:
                role = await self.guild.create_role(
                    name=name,
                    color=discord.Color(color),
                    hoist=hoist
                )
                print(f"  👑 Created role: {name}")
            except discord.HTTPException as e:
                print(f"  ❌ Failed to create role {name}: {e}")
        
        print("✅ Roles created!")
    
    async def send_announcement(self, message, channel_name="📢-announcements"):
        """Send announcement to specified channel"""
        channel = discord.utils.get(self.guild.channels, name=channel_name)
        if not channel:
            print(f"❌ Channel {channel_name} not found")
            return
        
        embed = discord.Embed(
            title="🚨 HOT PPL ANNOUNCEMENT",
            description=message,
            color=0xff0080,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="HOT PPL - Where the f*ck are all the hot people?")
        
        await channel.send(embed=embed)
        print(f"✅ Announcement sent to {channel_name}")
    
    async def post_submission(self, creator, scene, video_url, description=""):
        """Post a submission to the submissions channel"""
        channel = discord.utils.get(self.guild.channels, name="🎬-submissions")
        if not channel:
            print("❌ Submissions channel not found")
            return
        
        embed = discord.Embed(
            title=f"🎬 New Submission: {scene}",
            description=description,
            color=0xff0080
        )
        embed.add_field(name="👤 Creator", value=creator, inline=True)
        embed.add_field(name="🎭 Scene", value=scene, inline=True)
        embed.set_footer(text="React with 🔥 to vote!")
        
        if video_url:
            embed.add_field(name="🎥 Video", value=f"[Watch Here]({video_url})", inline=False)
        
        message = await channel.send(embed=embed)
        await message.add_reaction('🔥')
        
        print(f"✅ Submission posted for {creator}")
        return message.id
    
    async def update_leaderboard(self):
        """Update the leaderboard channel"""
        channel = discord.utils.get(self.guild.channels, name="🏆-leaderboard")
        if not channel:
            print("❌ Leaderboard channel not found")
            return
        
        # Clear channel
        await channel.purge()
        
        # Mock leaderboard data (replace with real data)
        leaderboard = [
            ("Minilambobae", "The Arrival", 156),
            ("AlienBecca", "DJ Reveal", 142),
            ("JennyFromSpace", "Tracksuit Encounter", 128),
            ("EarthlingMike", "Siri Consultation", 95),
            ("CosmicArt", "Final Judgment", 87)
        ]
        
        embed = discord.Embed(
            title="🏆 HOT PPL LEADERBOARD",
            description="Top submissions by votes",
            color=0x00ff88,
            timestamp=datetime.utcnow()
        )
        
        for i, (creator, scene, votes) in enumerate(leaderboard, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            embed.add_field(
                name=f"{medal} {creator}",
                value=f"**{scene}** • {votes} 🔥",
                inline=False
            )
        
        embed.set_footer(text="Updated automatically every 30 minutes")
        
        await channel.send(embed=embed)
        print("✅ Leaderboard updated")
    
    async def get_stats(self):
        """Get server statistics"""
        stats = {
            "server_name": self.guild.name,
            "member_count": self.guild.member_count,
            "channel_count": len(self.guild.channels),
            "role_count": len(self.guild.roles),
            "online_members": len([m for m in self.guild.members if m.status != discord.Status.offline])
        }
        
        print("📊 Server Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        return stats
    
    async def cleanup(self):
        """Clean up connection"""
        await self.client.close()

async def main():
    parser = argparse.ArgumentParser(description='HOT PPL Discord CLI')
    parser.add_argument('command', choices=[
        'setup', 'roles', 'announce', 'submit', 'leaderboard', 'stats'
    ], help='Command to execute')
    
    parser.add_argument('--message', help='Message for announcements')
    parser.add_argument('--creator', help='Creator name for submissions')
    parser.add_argument('--scene', help='Scene name for submissions')
    parser.add_argument('--video', help='Video URL for submissions')
    parser.add_argument('--description', help='Description for submissions')
    
    args = parser.parse_args()
    
    if not DISCORD_BOT_TOKEN:
        print("❌ DISCORD_BOT_TOKEN environment variable not set")
        return
    
    cli = DiscordCLI()
    
    try:
        await cli.connect()
        
        if args.command == 'setup':
            await cli.setup_server()
        
        elif args.command == 'roles':
            await cli.create_roles()
        
        elif args.command == 'announce':
            if not args.message:
                print("❌ --message required for announcements")
                return
            await cli.send_announcement(args.message)
        
        elif args.command == 'submit':
            if not all([args.creator, args.scene]):
                print("❌ --creator and --scene required for submissions")
                return
            await cli.post_submission(
                args.creator, 
                args.scene, 
                args.video or "", 
                args.description or ""
            )
        
        elif args.command == 'leaderboard':
            await cli.update_leaderboard()
        
        elif args.command == 'stats':
            await cli.get_stats()
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        await cli.cleanup()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
🛸 HOT PPL Discord CLI

Usage:
  python discord-cli.py setup                    # Set up server structure
  python discord-cli.py roles                    # Create roles
  python discord-cli.py announce --message "..."  # Send announcement
  python discord-cli.py submit --creator "..." --scene "..." --video "..."
  python discord-cli.py leaderboard              # Update leaderboard
  python discord-cli.py stats                    # Show server stats

Environment variables needed:
  DISCORD_BOT_TOKEN - Your Discord bot token
  DISCORD_GUILD_ID  - Your Discord server ID
        """)
    else:
        asyncio.run(main())
