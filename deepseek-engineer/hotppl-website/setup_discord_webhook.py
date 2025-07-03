#!/usr/bin/env python3
"""
Set up Discord webhook for HOT PPL submissions
This is easier than running a full bot on App Engine
"""

import discord
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', '0'))
SUBMISSION_CHANNEL_ID = int(os.getenv('SUBMISSION_CHANNEL_ID', '0'))

async def setup_webhook():
    """Set up Discord webhook for submissions"""
    print("🔧 Setting up Discord webhook for HOT PPL...")
    
    if not DISCORD_BOT_TOKEN:
        print("❌ No Discord bot token found!")
        return
    
    try:
        # Create client
        intents = discord.Intents.default()
        intents.guilds = True
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(f"✅ Connected as {client.user}")
            
            # Get guild and channel
            guild = client.get_guild(DISCORD_GUILD_ID)
            if not guild:
                print(f"❌ Could not find server with ID: {DISCORD_GUILD_ID}")
                await client.close()
                return
            
            channel = guild.get_channel(SUBMISSION_CHANNEL_ID)
            if not channel:
                print(f"❌ Could not find submission channel with ID: {SUBMISSION_CHANNEL_ID}")
                await client.close()
                return
            
            print(f"📝 Found submission channel: #{channel.name}")
            
            # Create webhook
            try:
                # Check if webhook already exists
                webhooks = await channel.webhooks()
                hotppl_webhook = None
                
                for webhook in webhooks:
                    if webhook.name == "HOT PPL Submissions":
                        hotppl_webhook = webhook
                        break
                
                if hotppl_webhook:
                    print(f"✅ Webhook already exists: {hotppl_webhook.url}")
                else:
                    # Create new webhook
                    hotppl_webhook = await channel.create_webhook(
                        name="HOT PPL Submissions",
                        reason="Automated submission posting from hotppl.io"
                    )
                    print(f"✅ Created new webhook: {hotppl_webhook.url}")
                
                # Save webhook URL to .env file
                webhook_url = hotppl_webhook.url
                
                # Update .env file
                env_lines = []
                webhook_found = False
                
                try:
                    with open('.env', 'r') as f:
                        env_lines = f.readlines()
                except FileNotFoundError:
                    pass
                
                # Update or add webhook URL
                for i, line in enumerate(env_lines):
                    if line.startswith('DISCORD_WEBHOOK_URL='):
                        env_lines[i] = f'DISCORD_WEBHOOK_URL={webhook_url}\n'
                        webhook_found = True
                        break
                
                if not webhook_found:
                    env_lines.append(f'DISCORD_WEBHOOK_URL={webhook_url}\n')
                
                # Write back to .env
                with open('.env', 'w') as f:
                    f.writelines(env_lines)
                
                print(f"✅ Webhook URL saved to .env file")
                
                # Test the webhook
                print("🧪 Testing webhook...")
                
                embed = discord.Embed(
                    title="🧪 Webhook Test",
                    description="HOT PPL Discord integration is working!",
                    color=0xff0080
                )
                embed.add_field(name="Status", value="✅ Connected", inline=True)
                embed.add_field(name="Website", value="hotppl.io", inline=True)
                embed.set_footer(text="HOT PPL - Where the f*ck are all the hot people?")
                
                await hotppl_webhook.send(embed=embed)
                print("✅ Webhook test successful!")
                
                print("\n🎉 Discord webhook setup complete!")
                print(f"📋 Webhook URL: {webhook_url}")
                print("\n🚀 Ready to deploy to Google Cloud with Discord integration!")
                
            except Exception as e:
                print(f"❌ Failed to create webhook: {e}")
            
            await client.close()
        
        # Connect to Discord
        await client.start(DISCORD_BOT_TOKEN)
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")

if __name__ == "__main__":
    asyncio.run(setup_webhook())
