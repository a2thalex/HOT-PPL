#!/usr/bin/env python3
"""
Quick Discord connection test
"""

import discord
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', '0'))

async def test_connection():
    """Test Discord bot connection"""
    print("🔍 Testing Discord Bot Connection...")
    print(f"Guild ID: {DISCORD_GUILD_ID}")
    print(f"Token configured: {'Yes' if DISCORD_BOT_TOKEN else 'No'}")
    
    if not DISCORD_BOT_TOKEN:
        print("❌ No Discord bot token found!")
        return False
    
    try:
        # Create client with minimal intents
        intents = discord.Intents.default()
        intents.guilds = True
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(f"✅ Bot connected as {client.user}")
            
            # Get guild info
            guild = client.get_guild(DISCORD_GUILD_ID)
            if guild:
                print(f"✅ Found server: {guild.name}")
                print(f"📊 Members: {guild.member_count}")
                print(f"📝 Channels: {len(guild.channels)}")
                
                # List existing channels
                print("\n📋 Existing Channels:")
                for channel in guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        print(f"  #{channel.name} (ID: {channel.id})")
            else:
                print(f"❌ Could not find server with ID: {DISCORD_GUILD_ID}")
            
            await client.close()
        
        # Connect to Discord
        await client.start(DISCORD_BOT_TOKEN)
        
    except discord.LoginFailure:
        print("❌ Invalid bot token!")
        return False
    except discord.HTTPException as e:
        print(f"❌ HTTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(test_connection())
