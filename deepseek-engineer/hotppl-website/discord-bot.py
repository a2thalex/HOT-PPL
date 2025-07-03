#!/usr/bin/env python3
"""
HOT PPL Discord Bot - Community Management & Voting System
This bot handles submissions, voting, leaderboards, and community features
"""

import discord
from discord.ext import commands, tasks
import asyncio
import json
import os
from datetime import datetime, timedelta
import aiohttp
import sqlite3
from typing import Optional, Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.reactions = True
# Don't require privileged intents for now

bot = commands.Bot(command_prefix='!hotppl ', intents=intents)

# Database setup
def init_database():
    conn = sqlite3.connect('hotppl_bot.db')
    cursor = conn.cursor()
    
    # Submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_user_id TEXT,
            username TEXT,
            scene TEXT,
            title TEXT,
            description TEXT,
            video_url TEXT,
            submission_time TIMESTAMP,
            vote_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending'
        )
    ''')
    
    # Votes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER,
            voter_discord_id TEXT,
            vote_time TIMESTAMP,
            FOREIGN KEY (submission_id) REFERENCES submissions (id),
            UNIQUE(submission_id, voter_discord_id)
        )
    ''')
    
    # User stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            discord_user_id TEXT PRIMARY KEY,
            username TEXT,
            submissions_count INTEGER DEFAULT 0,
            votes_given INTEGER DEFAULT 0,
            votes_received INTEGER DEFAULT 0,
            join_date TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

class HotPPLBot:
    def __init__(self):
        self.guild_id = int(os.getenv('DISCORD_GUILD_ID', '0'))
        self.submission_channel_id = int(os.getenv('SUBMISSION_CHANNEL_ID', '0'))
        self.voting_channel_id = int(os.getenv('VOTING_CHANNEL_ID', '0'))
        self.leaderboard_channel_id = int(os.getenv('LEADERBOARD_CHANNEL_ID', '0'))

# Add guild_id to bot instance
bot.guild_id = int(os.getenv('DISCORD_GUILD_ID', '0'))
bot.submission_channel_id = int(os.getenv('SUBMISSION_CHANNEL_ID', '0'))
bot.voting_channel_id = int(os.getenv('VOTING_CHANNEL_ID', '0'))
bot.leaderboard_channel_id = int(os.getenv('LEADERBOARD_CHANNEL_ID', '0'))
        
    async def setup_channels(self, guild):
        """Set up necessary channels and roles"""
        # Create submission channel if it doesn't exist
        submission_channel = discord.utils.get(guild.channels, name='🎬-submissions')
        if not submission_channel:
            submission_channel = await guild.create_text_channel(
                '🎬-submissions',
                topic='Submit your HOT PPL scene recreations here!'
            )
        
        # Create voting channel
        voting_channel = discord.utils.get(guild.channels, name='🗳️-voting')
        if not voting_channel:
            voting_channel = await guild.create_text_channel(
                '🗳️-voting',
                topic='Vote on submissions here! React with 🔥 to vote!'
            )
        
        # Create leaderboard channel
        leaderboard_channel = discord.utils.get(guild.channels, name='🏆-leaderboard')
        if not leaderboard_channel:
            leaderboard_channel = await guild.create_text_channel(
                '🏆-leaderboard',
                topic='Current rankings and top creators'
            )
        
        return submission_channel, voting_channel, leaderboard_channel

@bot.event
async def on_ready():
    print(f'{bot.user} has landed on Earth! 🛸')
    init_database()
    
    # Set up channels
    guild = bot.get_guild(bot.guild_id) if bot.guild_id else bot.guilds[0]
    if guild:
        await bot.setup_channels(guild)
    
    # Start periodic tasks
    update_leaderboard.start()
    check_new_submissions.start()

@bot.command(name='submit')
async def submit_scene(ctx, scene: str, *, description: str = ""):
    """Submit a scene recreation"""
    user_id = str(ctx.author.id)
    username = ctx.author.display_name
    
    # Check if user has attached a video
    if not ctx.message.attachments:
        await ctx.reply("❌ Please attach your video file when submitting!")
        return
    
    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(('.mp4', '.mov', '.avi')):
        await ctx.reply("❌ Please submit a video file (MP4, MOV, or AVI)")
        return
    
    # Save submission to database
    conn = sqlite3.connect('hotppl_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO submissions (discord_user_id, username, scene, description, video_url, submission_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, username, scene, description, attachment.url, datetime.now()))
    
    submission_id = cursor.lastrowid
    
    # Update user stats
    cursor.execute('''
        INSERT OR REPLACE INTO user_stats (discord_user_id, username, submissions_count, join_date)
        VALUES (?, ?, COALESCE((SELECT submissions_count FROM user_stats WHERE discord_user_id = ?) + 1, 1), ?)
    ''', (user_id, username, user_id, datetime.now()))
    
    conn.commit()
    conn.close()
    
    # Create voting embed
    embed = discord.Embed(
        title=f"🎬 New Submission: {scene}",
        description=description,
        color=0xff0080
    )
    embed.add_field(name="Creator", value=username, inline=True)
    embed.add_field(name="Scene", value=scene, inline=True)
    embed.add_field(name="Submission ID", value=f"#{submission_id}", inline=True)
    embed.set_author(name=username, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    embed.set_image(url=attachment.url)
    embed.set_footer(text="React with 🔥 to vote! • HOT PPL")
    
    # Post to voting channel
    voting_channel = bot.get_channel(bot.voting_channel_id)
    if voting_channel:
        vote_message = await voting_channel.send(embed=embed)
        await vote_message.add_reaction('🔥')
        
        # Store message ID for vote tracking
        conn = sqlite3.connect('hotppl_bot.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE submissions SET vote_message_id = ? WHERE id = ?', 
                      (vote_message.id, submission_id))
        conn.commit()
        conn.close()
    
    await ctx.reply(f"✅ Submission received! Check {voting_channel.mention} to see it live!")

@bot.event
async def on_reaction_add(reaction, user):
    """Handle voting reactions"""
    if user.bot:
        return
    
    if str(reaction.emoji) == '🔥' and reaction.message.channel.id == bot.voting_channel_id:
        # This is a vote!
        message_id = reaction.message.id
        voter_id = str(user.id)
        
        # Find submission by message ID
        conn = sqlite3.connect('hotppl_bot.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM submissions WHERE vote_message_id = ?', (message_id,))
        result = cursor.fetchone()
        
        if result:
            submission_id = result[0]
            
            # Check if user already voted
            cursor.execute('SELECT id FROM votes WHERE submission_id = ? AND voter_discord_id = ?',
                          (submission_id, voter_id))
            
            if not cursor.fetchone():
                # Add vote
                cursor.execute('''
                    INSERT INTO votes (submission_id, voter_discord_id, vote_time)
                    VALUES (?, ?, ?)
                ''', (submission_id, voter_id, datetime.now()))
                
                # Update vote count
                cursor.execute('''
                    UPDATE submissions SET vote_count = vote_count + 1 WHERE id = ?
                ''', (submission_id,))
                
                # Update voter stats
                cursor.execute('''
                    INSERT OR REPLACE INTO user_stats (discord_user_id, username, votes_given)
                    VALUES (?, ?, COALESCE((SELECT votes_given FROM user_stats WHERE discord_user_id = ?) + 1, 1))
                ''', (voter_id, user.display_name, voter_id))
                
                conn.commit()
        
        conn.close()

@bot.command(name='leaderboard')
async def show_leaderboard(ctx):
    """Show current leaderboard"""
    conn = sqlite3.connect('hotppl_bot.db')
    cursor = conn.cursor()
    
    # Get top submissions
    cursor.execute('''
        SELECT username, scene, vote_count, submission_time
        FROM submissions
        ORDER BY vote_count DESC, submission_time ASC
        LIMIT 10
    ''')
    
    submissions = cursor.fetchall()
    
    embed = discord.Embed(
        title="🏆 HOT PPL Leaderboard",
        description="Top submissions by votes",
        color=0x00ff88
    )
    
    for i, (username, scene, votes, time) in enumerate(submissions, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        embed.add_field(
            name=f"{medal} {username}",
            value=f"**{scene}** • {votes} 🔥",
            inline=False
        )
    
    conn.close()
    await ctx.send(embed=embed)

@bot.command(name='stats')
async def user_stats(ctx, member: Optional[discord.Member] = None):
    """Show user statistics"""
    target = member or ctx.author
    user_id = str(target.id)
    
    conn = sqlite3.connect('hotppl_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT submissions_count, votes_given, votes_received
        FROM user_stats
        WHERE discord_user_id = ?
    ''', (user_id,))
    
    result = cursor.fetchone()
    
    if result:
        submissions, votes_given, votes_received = result
        
        embed = discord.Embed(
            title=f"📊 Stats for {target.display_name}",
            color=0x00d4ff
        )
        embed.add_field(name="🎬 Submissions", value=submissions, inline=True)
        embed.add_field(name="🔥 Votes Given", value=votes_given, inline=True)
        embed.add_field(name="❤️ Votes Received", value=votes_received, inline=True)
        embed.set_thumbnail(url=target.avatar.url if target.avatar else None)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{target.display_name} hasn't participated yet!")
    
    conn.close()

@tasks.loop(minutes=30)
async def update_leaderboard():
    """Update leaderboard channel periodically"""
    if not bot.leaderboard_channel_id:
        return
    
    channel = bot.get_channel(bot.leaderboard_channel_id)
    if not channel:
        return
    
    # Clear channel and post updated leaderboard
    await channel.purge()
    
    conn = sqlite3.connect('hotppl_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT username, scene, vote_count, submission_time
        FROM submissions
        ORDER BY vote_count DESC, submission_time ASC
        LIMIT 10
    ''')
    
    submissions = cursor.fetchall()
    
    embed = discord.Embed(
        title="🏆 LIVE LEADERBOARD",
        description="Updated every 30 minutes",
        color=0x00ff88,
        timestamp=datetime.now()
    )
    
    for i, (username, scene, votes, time) in enumerate(submissions, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        embed.add_field(
            name=f"{medal} {username}",
            value=f"**{scene}** • {votes} 🔥",
            inline=False
        )
    
    embed.set_footer(text="HOT PPL - Where the f*ck are all the hot people?")
    
    await channel.send(embed=embed)
    conn.close()

@tasks.loop(minutes=5)
async def check_new_submissions():
    """Check for new submissions from website"""
    # This would integrate with your website's API
    # to automatically post submissions from the web form
    pass

# Run the bot
if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
