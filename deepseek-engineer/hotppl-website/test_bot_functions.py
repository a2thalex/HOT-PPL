#!/usr/bin/env python3
"""
Test all Discord bot functions
"""

import discord
import asyncio
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', '0'))
SUBMISSION_CHANNEL_ID = int(os.getenv('SUBMISSION_CHANNEL_ID', '0'))
VOTING_CHANNEL_ID = int(os.getenv('VOTING_CHANNEL_ID', '0'))
LEADERBOARD_CHANNEL_ID = int(os.getenv('LEADERBOARD_CHANNEL_ID', '0'))

async def test_bot_functions():
    """Test all Discord bot functions"""
    print("🧪 Testing Discord Bot Functions...")
    
    # Initialize database
    print("📊 Initializing database...")
    init_database()
    
    try:
        # Create client with minimal intents
        intents = discord.Intents.default()
        intents.guilds = True
        intents.reactions = True
        # Don't require privileged intents for now
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(f"✅ Bot connected as {client.user}")
            
            guild = client.get_guild(DISCORD_GUILD_ID)
            if not guild:
                print(f"❌ Could not find server with ID: {DISCORD_GUILD_ID}")
                await client.close()
                return
            
            print(f"✅ Connected to server: {guild.name}")
            
            # Test channel access
            submission_channel = client.get_channel(SUBMISSION_CHANNEL_ID)
            voting_channel = client.get_channel(VOTING_CHANNEL_ID)
            leaderboard_channel = client.get_channel(LEADERBOARD_CHANNEL_ID)
            
            print(f"📝 Submission channel: {submission_channel.name if submission_channel else 'NOT FOUND'}")
            print(f"🗳️ Voting channel: {voting_channel.name if voting_channel else 'NOT FOUND'}")
            print(f"🏆 Leaderboard channel: {leaderboard_channel.name if leaderboard_channel else 'NOT FOUND'}")
            
            # Test database operations
            print("\n🗄️ Testing database operations...")
            test_database_operations()
            
            # Test posting to channels
            if submission_channel:
                print("\n📤 Testing channel posting...")
                try:
                    embed = discord.Embed(
                        title="🧪 Bot Function Test",
                        description="Testing Discord bot integration",
                        color=0xff0080
                    )
                    embed.add_field(name="Status", value="✅ All systems operational", inline=False)
                    embed.add_field(name="Timestamp", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), inline=False)
                    embed.set_footer(text="HOT PPL Bot Test")
                    
                    message = await submission_channel.send(embed=embed)
                    print(f"✅ Successfully posted test message to #{submission_channel.name}")
                    
                    # Test reactions
                    await message.add_reaction('🔥')
                    print("✅ Successfully added reaction")
                    
                except Exception as e:
                    print(f"❌ Error posting to channel: {e}")
            
            # Test leaderboard generation
            if leaderboard_channel:
                print("\n🏆 Testing leaderboard generation...")
                try:
                    await generate_test_leaderboard(leaderboard_channel)
                    print("✅ Successfully generated test leaderboard")
                except Exception as e:
                    print(f"❌ Error generating leaderboard: {e}")
            
            print("\n✅ All bot function tests completed!")
            await client.close()
        
        # Connect to Discord
        await client.start(DISCORD_BOT_TOKEN)
        
    except Exception as e:
        print(f"❌ Bot test error: {e}")
        return False
    
    return True

def init_database():
    """Initialize the database"""
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
            status TEXT DEFAULT 'pending',
            vote_message_id TEXT
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
    print("✅ Database initialized successfully")

def test_database_operations():
    """Test database operations"""
    conn = sqlite3.connect('hotppl_bot.db')
    cursor = conn.cursor()
    
    # Test submission insertion
    cursor.execute('''
        INSERT INTO submissions (discord_user_id, username, scene, description, submission_time, vote_count)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('test_user_123', 'TestUser', 'THE ARRIVAL', 'Test submission for bot testing', datetime.now(), 5))
    
    submission_id = cursor.lastrowid
    
    # Test vote insertion
    cursor.execute('''
        INSERT INTO votes (submission_id, voter_discord_id, vote_time)
        VALUES (?, ?, ?)
    ''', (submission_id, 'voter_123', datetime.now()))
    
    # Test user stats
    cursor.execute('''
        INSERT OR REPLACE INTO user_stats (discord_user_id, username, submissions_count, votes_given, join_date)
        VALUES (?, ?, ?, ?, ?)
    ''', ('test_user_123', 'TestUser', 1, 0, datetime.now()))
    
    conn.commit()
    
    # Test queries
    cursor.execute('SELECT COUNT(*) FROM submissions')
    submission_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM votes')
    vote_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM user_stats')
    user_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"✅ Database test: {submission_count} submissions, {vote_count} votes, {user_count} users")

async def generate_test_leaderboard(channel):
    """Generate a test leaderboard"""
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
        title="🏆 HOT PPL LEADERBOARD (TEST)",
        description="Current top submissions",
        color=0x00ff88,
        timestamp=datetime.now()
    )
    
    if submissions:
        for i, (username, scene, votes, time) in enumerate(submissions, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            embed.add_field(
                name=f"{medal} {username}",
                value=f"**{scene}** • {votes} 🔥",
                inline=False
            )
    else:
        embed.add_field(name="No submissions yet", value="Be the first to submit!", inline=False)
    
    embed.set_footer(text="HOT PPL - Where the f*ck are all the hot people?")
    
    await channel.send(embed=embed)
    conn.close()

if __name__ == "__main__":
    asyncio.run(test_bot_functions())
