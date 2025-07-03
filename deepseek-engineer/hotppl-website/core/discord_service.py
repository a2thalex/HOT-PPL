#!/usr/bin/env python3
"""
HOT PPL Discord Service
Comprehensive Discord integration service for the platform
"""

import discord
from discord.ext import commands, tasks
import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import aiohttp
from dotenv import load_dotenv

from database import db, User, Submission, SubmissionStatus, UserRole

load_dotenv()

class AdvancedDiscordService:
    def __init__(self):
        # Discord configuration
        self.bot_token = os.getenv('DISCORD_BOT_TOKEN')
        self.guild_id = int(os.getenv('DISCORD_GUILD_ID', '0'))
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        # Bot setup
        intents = discord.Intents.default()
        intents.reactions = True
        intents.guilds = True
        
        self.bot = commands.Bot(command_prefix='!hotppl ', intents=intents)
        self.guild = None
        self.channels = {}
        self.roles = {}
        
        # Setup bot events
        self.setup_bot_events()
        
        # Connection status
        self._connected = False
    
    def setup_bot_events(self):
        """Setup Discord bot events"""
        
        @self.bot.event
        async def on_ready():
            print(f'🛸 {self.bot.user} has connected to Discord!')
            self.guild = self.bot.get_guild(self.guild_id)
            if self.guild:
                self._connected = True  # Set connected first
                print(f'✅ Connected to {self.guild.name}')
                await self.setup_server_infrastructure()
                print('✅ Discord server infrastructure setup complete!')
            else:
                print(f'❌ Could not find guild {self.guild_id}')
        
        @self.bot.event
        async def on_reaction_add(reaction, user):
            """Handle voting reactions"""
            if user.bot:
                return
            
            await self.process_vote_reaction(reaction, user, 'add')
        
        @self.bot.event
        async def on_reaction_remove(reaction, user):
            """Handle vote removal"""
            if user.bot:
                return
            
            await self.process_vote_reaction(reaction, user, 'remove')
        
        @self.bot.command(name='submit')
        async def submit_command(ctx, scene: str, *, description: str = ""):
            """Submit a scene recreation via Discord"""
            await self.handle_discord_submission(ctx, scene, description)
        
        @self.bot.command(name='leaderboard')
        async def leaderboard_command(ctx):
            """Show current leaderboard"""
            await self.send_leaderboard(ctx.channel)
        
        @self.bot.command(name='stats')
        async def stats_command(ctx, member: discord.Member = None):
            """Show user statistics"""
            target = member or ctx.author
            await self.send_user_stats(ctx.channel, target)
    
    async def setup_server_infrastructure(self):
        """Set up comprehensive Discord server structure"""
        if not self.guild:
            return
        
        # Server structure
        server_structure = {
            "📋 INFORMATION": {
                "channels": [
                    ("📢-announcements", "Official HOT PPL announcements"),
                    ("📖-rules", "Server rules and community guidelines"),
                    ("🎯-current-challenge", "Active music video challenge info"),
                    ("🏆-hall-of-fame", "Best submissions of all time")
                ],
                "type": "info"
            },
            "🎬 CREATION HUB": {
                "channels": [
                    ("🎬-submissions", "Submit your scene recreations"),
                    ("🗳️-voting-gallery", "Vote on submissions with reactions"),
                    ("💬-feedback-lounge", "Detailed feedback and discussions"),
                    ("🤝-collaborations", "Find partners and team up")
                ],
                "type": "creation"
            },
            "📊 LIVE ANALYTICS": {
                "channels": [
                    ("🏆-live-leaderboard", "Real-time rankings (auto-updated)"),
                    ("📈-platform-stats", "Community growth and engagement"),
                    ("🔥-trending-now", "Hot submissions and viral content"),
                    ("📊-creator-insights", "Analytics for top creators")
                ],
                "type": "analytics"
            },
            "🎉 COMMUNITY": {
                "channels": [
                    ("💬-general-chat", "General community discussions"),
                    ("🎨-inspiration-board", "Share ideas and references"),
                    ("🛠️-creator-resources", "Tools, tips, and tutorials"),
                    ("🎤-voice-hangout", "Voice chat for creators")
                ],
                "type": "community"
            },
            "🔒 VIP ZONE": {
                "channels": [
                    ("👑-top-creators", "Exclusive chat for top 10 creators"),
                    ("🎭-behind-the-scenes", "Creator process and insights"),
                    ("🚀-early-access", "New features and challenges first"),
                    ("💎-vip-lounge", "Premium creator discussions")
                ],
                "type": "vip"
            }
        }
        
        # Create categories and channels
        for category_name, category_data in server_structure.items():
            category = await self.get_or_create_category(category_name)
            
            for channel_name, topic in category_data["channels"]:
                if channel_name == "🎤-voice-hangout":
                    channel = await self.get_or_create_voice_channel(channel_name, category)
                else:
                    channel = await self.get_or_create_text_channel(channel_name, category, topic)
                
                # Store channel references
                clean_name = channel_name.replace('🎬-', '').replace('🗳️-', '').replace('🏆-', '')
                self.channels[clean_name] = channel
        
        # Create roles
        await self.setup_roles()
        
        print("✅ Discord server infrastructure setup complete!")
    
    async def get_or_create_category(self, name: str):
        """Get existing category or create new one"""
        category = discord.utils.get(self.guild.categories, name=name)
        if not category:
            category = await self.guild.create_category(name)
            print(f"📁 Created category: {name}")
        return category
    
    async def get_or_create_text_channel(self, name: str, category, topic: str = None):
        """Get existing text channel or create new one"""
        channel = discord.utils.get(self.guild.channels, name=name)
        if not channel:
            channel = await self.guild.create_text_channel(
                name, category=category, topic=topic
            )
            print(f"📝 Created channel: {name}")
        return channel
    
    async def get_or_create_voice_channel(self, name: str, category):
        """Get existing voice channel or create new one"""
        channel = discord.utils.get(self.guild.voice_channels, name=name)
        if not channel:
            channel = await self.guild.create_voice_channel(name, category=category)
            print(f"🎤 Created voice channel: {name}")
        return channel
    
    async def setup_roles(self):
        """Create and configure user roles"""
        role_config = [
            ("🛸 Alien Admin", 0xff0080, True, ["administrator"]),
            ("🎬 Top Creator", 0x00ff88, True, ["manage_messages"]),
            ("✅ Verified Creator", 0x00d4ff, False, ["embed_links"]),
            ("🤝 Community Helper", 0x8000ff, False, ["manage_messages"]),
            ("🎭 Scene Master", 0xff4000, False, ["embed_links"]),
            ("👽 Earthling", 0x666666, False, [])
        ]
        
        for name, color, hoist, permissions in role_config:
            role = discord.utils.get(self.guild.roles, name=name)
            if not role:
                perms = discord.Permissions()
                for perm in permissions:
                    setattr(perms, perm, True)
                
                role = await self.guild.create_role(
                    name=name,
                    color=discord.Color(color),
                    hoist=hoist,
                    permissions=perms
                )
                print(f"👑 Created role: {name}")
            
            self.roles[name] = role
    
    async def post_submission(self, submission: Submission, user: User) -> Dict:
        """Post submission to Discord with rich embed"""
        if not self.channels.get('submissions'):
            return {'success': False, 'error': 'Submissions channel not found'}
        
        # Create rich embed
        embed = discord.Embed(
            title=f"🎬 {submission.title}",
            description=submission.description,
            color=0xff0080,
            timestamp=submission.created_at
        )
        
        embed.add_field(name="👤 Creator", value=user.username, inline=True)
        embed.add_field(name="🎭 Scene", value=submission.scene_name, inline=True)
        embed.add_field(name="🛠️ Tools", value=", ".join(submission.tools_used) or "Not specified", inline=True)
        
        if submission.video_url:
            embed.add_field(name="🎥 Video", value=f"[Watch Here]({submission.video_url})", inline=False)
        
        embed.set_footer(text="React with 🔥 to vote! • HOT PPL")
        
        try:
            message = await self.channels['submissions'].send(embed=embed)
            
            # Add voting reactions
            await message.add_reaction('🔥')
            await message.add_reaction('❤️')
            await message.add_reaction('🤯')
            
            # Update database with Discord message ID
            # db.update_submission_discord_id(submission.id, message.id)
            
            return {
                'success': True,
                'message_id': str(message.id),
                'channel_id': str(message.channel.id)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def process_vote_reaction(self, reaction, user, action: str):
        """Process voting reactions"""
        # Map emoji to vote types
        vote_map = {
            '🔥': 'fire',
            '❤️': 'love', 
            '🤯': 'mind_blown'
        }
        
        if str(reaction.emoji) not in vote_map:
            return
        
        vote_type = vote_map[str(reaction.emoji)]
        
        # Find submission by message ID
        # Update vote count
        # Update leaderboard
        # Log analytics
        
        print(f"Vote {action}: {user.name} voted {vote_type} on message {reaction.message.id}")
    
    async def send_leaderboard(self, channel):
        """Send current leaderboard to channel"""
        leaderboard = db.get_leaderboard(10)
        
        embed = discord.Embed(
            title="🏆 HOT PPL LEADERBOARD",
            description="Top submissions by community votes",
            color=0x00ff88,
            timestamp=datetime.now()
        )
        
        for i, entry in enumerate(leaderboard, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            embed.add_field(
                name=f"{medal} {entry['username']}",
                value=f"**{entry['scene_name']}** • {entry['vote_count']} 🔥",
                inline=False
            )
        
        embed.set_footer(text="Updated in real-time • HOT PPL")
        
        await channel.send(embed=embed)
    
    async def send_user_stats(self, channel, discord_user):
        """Send user statistics"""
        user = db.get_user_by_discord_id(str(discord_user.id))
        
        if not user:
            await channel.send(f"{discord_user.mention} hasn't participated yet!")
            return
        
        embed = discord.Embed(
            title=f"📊 Stats for {user.username}",
            color=0x00d4ff,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="🎬 Submissions", value=user.total_submissions, inline=True)
        embed.add_field(name="🔥 Votes Given", value=user.total_votes_given, inline=True)
        embed.add_field(name="❤️ Votes Received", value=user.total_votes_received, inline=True)
        embed.add_field(name="⭐ Reputation", value=user.reputation_score, inline=True)
        embed.add_field(name="👑 Role", value=user.role.value.replace('_', ' ').title(), inline=True)
        embed.add_field(name="✅ Verified", value="Yes" if user.is_verified else "No", inline=True)
        
        embed.set_thumbnail(url=discord_user.avatar.url if discord_user.avatar else None)
        
        await channel.send(embed=embed)
    
    def is_connected(self) -> bool:
        """Check if Discord service is connected"""
        return self._connected and self.bot.is_ready()
    
    async def start(self):
        """Start the Discord service"""
        if self.bot_token:
            await self.bot.start(self.bot_token)
        else:
            print("❌ Discord bot token not configured")
    
    async def stop(self):
        """Stop the Discord service"""
        await self.bot.close()

# Global Discord service instance
discord_service = AdvancedDiscordService()
