#!/usr/bin/env python3
"""
Quick test to validate Discord bot token format
"""

import os
from dotenv import load_dotenv
import base64

load_dotenv()

token = os.getenv('DISCORD_BOT_TOKEN')
guild_id = os.getenv('DISCORD_GUILD_ID')

print("🔍 Discord Configuration Check")
print("=" * 40)

print(f"Guild ID: {guild_id}")
print(f"Token length: {len(token) if token else 0}")
print(f"Token starts with: {token[:10] if token else 'None'}...")

# Discord bot tokens have a specific format
if token:
    try:
        # Discord bot tokens are base64 encoded and contain the bot ID
        parts = token.split('.')
        if len(parts) >= 2:
            # First part should be the bot ID in base64
            bot_id_b64 = parts[0]
            # Add padding if needed
            padding = 4 - len(bot_id_b64) % 4
            if padding != 4:
                bot_id_b64 += '=' * padding
            
            try:
                bot_id = base64.b64decode(bot_id_b64).decode('utf-8')
                print(f"Extracted Bot ID: {bot_id}")
                
                # Check if this matches the application ID
                if bot_id == guild_id:
                    print("⚠️ Bot ID matches Guild ID - this might be wrong")
                else:
                    print("✅ Bot ID looks different from Guild ID - good")
                    
            except:
                print("❌ Could not decode bot ID from token")
        else:
            print("❌ Token doesn't have expected format (should have dots)")
            
    except Exception as e:
        print(f"❌ Token validation error: {e}")

print("\n📋 Expected format:")
print("Bot Token should look like: MTM4NjA0NzIzMjQxMDkxMDg2MA.GxxxXx.xxxxxxxxxxxxxxxxxxxxxxxxxx")
print("Guild ID should be: 1386047232410910860")
print("\n🔧 To get the correct bot token:")
print("1. Go to https://discord.com/developers/applications")
print("2. Select your HOT PPL Bot application")
print("3. Go to 'Bot' section")
print("4. Click 'Reset Token' and copy the new token")
