#!/usr/bin/env python3
"""
Generate Discord bot invite link for HOT PPL Bot
"""

import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('DISCORD_CLIENT_ID', '1386047232410910860')

# Required permissions for HOT PPL bot
permissions = [
    'send_messages',           # 2048
    'manage_messages',         # 8192  
    'embed_links',            # 16384
    'attach_files',           # 32768
    'read_message_history',   # 65536
    'add_reactions',          # 64
    'use_slash_commands',     # 2147483648
    'manage_channels',        # 16
    'manage_roles',           # 268435456
]

# Calculate permission integer
permission_int = (
    2048 +      # send_messages
    8192 +      # manage_messages  
    16384 +     # embed_links
    32768 +     # attach_files
    65536 +     # read_message_history
    64 +        # add_reactions
    2147483648 + # use_slash_commands
    16 +        # manage_channels
    268435456   # manage_roles
)

# Generate invite URL
invite_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={permission_int}&scope=bot%20applications.commands"

print("🤖 HOT PPL Discord Bot Invite")
print("=" * 40)
print(f"Client ID: {client_id}")
print(f"Permissions: {permission_int}")
print()
print("🔗 Bot Invite URL:")
print(invite_url)
print()
print("📋 Steps:")
print("1. Click the URL above (or copy/paste into browser)")
print("2. Select your HOT PPL Discord server")
print("3. Click 'Authorize'")
print("4. Bot will join your server with admin permissions")
print()
print("✅ After inviting, the bot will be ready to deploy!")

# Also save to file
with open('bot-invite-url.txt', 'w') as f:
    f.write(invite_url)

print("💾 Invite URL saved to: bot-invite-url.txt")
