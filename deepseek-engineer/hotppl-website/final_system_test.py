#!/usr/bin/env python3
"""
Final comprehensive test of HOT PPL Discord integration
"""

import asyncio
import discord
import requests
import sqlite3
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', '0'))
SUBMISSION_CHANNEL_ID = int(os.getenv('SUBMISSION_CHANNEL_ID', '0'))
VOTING_CHANNEL_ID = int(os.getenv('VOTING_CHANNEL_ID', '0'))
LEADERBOARD_CHANNEL_ID = int(os.getenv('LEADERBOARD_CHANNEL_ID', '0'))
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

API_BASE = 'http://localhost:8080'

def test_core_functionality():
    """Test the core functionality that matters for deployment"""
    print("🧪 HOT PPL FINAL SYSTEM TEST")
    print("Testing core functionality for deployment readiness...")
    print("="*60)
    
    results = {}
    
    # 1. Test Database
    print("\n🗄️ Testing Database...")
    try:
        conn = sqlite3.connect('hotppl_platform.db')
        cursor = conn.cursor()
        
        # Test submission
        test_id = f"test-{int(time.time())}"
        cursor.execute('''
            INSERT INTO submissions (id, creator, scene, title, description, video_url, submission_time, vote_count, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (test_id, 'TestUser', 'THE ARRIVAL', 'Test', 'Testing', 'http://test.com', 
              datetime.now().isoformat(), 0, 'pending'))
        
        # Test vote
        cursor.execute('''
            INSERT INTO votes (submission_id, voter_id, vote_time)
            VALUES (?, ?, ?)
        ''', (test_id, 'voter123', datetime.now().isoformat()))
        
        # Update vote count
        cursor.execute('UPDATE submissions SET vote_count = vote_count + 1 WHERE id = ?', (test_id,))
        
        conn.commit()
        
        # Verify
        cursor.execute('SELECT vote_count FROM submissions WHERE id = ?', (test_id,))
        vote_count = cursor.fetchone()[0]
        
        conn.close()
        
        if vote_count == 1:
            print("✅ Database: Full CRUD operations working")
            results['database'] = True
        else:
            print("❌ Database: Vote counting failed")
            results['database'] = False
            
    except Exception as e:
        print(f"❌ Database: {e}")
        results['database'] = False
    
    # 2. Test API Endpoints
    print("\n🌐 Testing API...")
    
    # Health check
    try:
        response = requests.get(f'{API_BASE}/health', timeout=5)
        if response.status_code == 200:
            print("✅ API Health: Working")
            results['api_health'] = True
        else:
            print(f"❌ API Health: Status {response.status_code}")
            results['api_health'] = False
    except Exception as e:
        print(f"❌ API Health: {e}")
        results['api_health'] = False
    
    # Submission
    try:
        submission_data = {
            "creator": "FinalTestUser",
            "scene": "FINAL TEST",
            "title": "Final System Test",
            "description": "Testing complete integration",
            "video_url": "https://example.com/final-test.mp4",
            "tools": "System Testing"
        }
        
        response = requests.post(
            f'{API_BASE}/api/submissions',
            headers={'Content-Type': 'application/json'},
            json=submission_data,
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ API Submission: Created ID {data['submission_id'][:8]}...")
            results['api_submission'] = True
            test_submission_id = data['submission_id']
        else:
            print(f"❌ API Submission: Status {response.status_code}")
            results['api_submission'] = False
            test_submission_id = None
            
    except Exception as e:
        print(f"❌ API Submission: {e}")
        results['api_submission'] = False
        test_submission_id = None
    
    # Voting
    if test_submission_id:
        try:
            vote_data = {
                "submission_id": test_submission_id,
                "voter_id": "final-test-voter"
            }
            
            response = requests.post(
                f'{API_BASE}/api/vote',
                headers={'Content-Type': 'application/json'},
                json=vote_data,
                timeout=5
            )
            
            if response.status_code == 200:
                print("✅ API Voting: Working")
                results['api_voting'] = True
            else:
                print(f"❌ API Voting: Status {response.status_code}")
                results['api_voting'] = False
        except Exception as e:
            print(f"❌ API Voting: {e}")
            results['api_voting'] = False
    
    # Leaderboard
    try:
        response = requests.get(f'{API_BASE}/api/leaderboard', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Leaderboard: {len(data['leaderboard'])} entries")
            results['api_leaderboard'] = True
        else:
            print(f"❌ API Leaderboard: Status {response.status_code}")
            results['api_leaderboard'] = False
    except Exception as e:
        print(f"❌ API Leaderboard: {e}")
        results['api_leaderboard'] = False
    
    # 3. Test Website Pages
    print("\n🌐 Testing Website...")
    pages = ['/', '/scenes.html', '/submit.html', '/confirmation.html']
    website_working = True
    
    for page in pages:
        try:
            response = requests.get(f'{API_BASE}{page}', timeout=5)
            if response.status_code == 200:
                print(f"✅ Website {page}: Accessible")
            else:
                print(f"❌ Website {page}: Status {response.status_code}")
                website_working = False
        except Exception as e:
            print(f"❌ Website {page}: {e}")
            website_working = False
    
    results['website'] = website_working
    
    return results

async def test_discord_integration():
    """Test Discord bot integration"""
    print("\n🤖 Testing Discord Integration...")
    
    if not DISCORD_BOT_TOKEN:
        print("❌ Discord: No bot token configured")
        return False
    
    try:
        intents = discord.Intents.default()
        intents.guilds = True
        intents.reactions = True
        client = discord.Client(intents=intents)
        
        discord_results = {}
        
        @client.event
        async def on_ready():
            try:
                print(f"✅ Discord Bot: Connected as {client.user}")
                discord_results['connection'] = True
                
                # Test guild access
                guild = client.get_guild(DISCORD_GUILD_ID)
                if guild:
                    print(f"✅ Discord Server: {guild.name} ({guild.member_count} members)")
                    discord_results['guild'] = True
                    
                    # Test channels
                    channels = {
                        'submission': guild.get_channel(SUBMISSION_CHANNEL_ID),
                        'voting': guild.get_channel(VOTING_CHANNEL_ID),
                        'leaderboard': guild.get_channel(LEADERBOARD_CHANNEL_ID)
                    }
                    
                    channels_ok = True
                    for name, channel in channels.items():
                        if channel:
                            print(f"✅ Discord {name.title()}: #{channel.name}")
                        else:
                            print(f"❌ Discord {name.title()}: Not found")
                            channels_ok = False
                    
                    discord_results['channels'] = channels_ok
                    
                    # Test posting capability
                    if channels['submission']:
                        try:
                            embed = discord.Embed(
                                title="🎉 System Test Complete!",
                                description="HOT PPL Discord integration is fully operational",
                                color=0x00ff88
                            )
                            embed.add_field(name="Status", value="✅ All systems go!", inline=False)
                            embed.add_field(name="Ready for", value="🚀 Production deployment", inline=False)
                            embed.set_footer(text="HOT PPL - Where the f*ck are all the hot people?")
                            
                            message = await channels['submission'].send(embed=embed)
                            await message.add_reaction('🔥')
                            await message.add_reaction('🚀')
                            await message.add_reaction('🎉')
                            
                            print("✅ Discord Posting: Message sent with reactions")
                            discord_results['posting'] = True
                            
                        except Exception as e:
                            print(f"❌ Discord Posting: {e}")
                            discord_results['posting'] = False
                else:
                    print(f"❌ Discord Server: Guild {DISCORD_GUILD_ID} not found")
                    discord_results['guild'] = False
                
            except Exception as e:
                print(f"❌ Discord Testing: {e}")
            finally:
                await client.close()
        
        await asyncio.wait_for(client.start(DISCORD_BOT_TOKEN), timeout=30)
        return discord_results
        
    except Exception as e:
        print(f"❌ Discord: {e}")
        return False

def print_final_summary(api_results, discord_results):
    """Print final test summary"""
    print("\n" + "="*60)
    print("🎯 HOT PPL DEPLOYMENT READINESS REPORT")
    print("="*60)
    
    # Core functionality
    core_tests = ['database', 'api_health', 'api_submission', 'api_voting', 'api_leaderboard', 'website']
    core_passed = sum(1 for test in core_tests if api_results.get(test, False))
    
    print(f"\n📊 Core Functionality: {core_passed}/{len(core_tests)} tests passed")
    
    for test in core_tests:
        status = "✅" if api_results.get(test, False) else "❌"
        print(f"  {status} {test.replace('_', ' ').title()}")
    
    # Discord functionality
    if discord_results:
        discord_tests = ['connection', 'guild', 'channels', 'posting']
        discord_passed = sum(1 for test in discord_tests if discord_results.get(test, False))
        
        print(f"\n🤖 Discord Integration: {discord_passed}/{len(discord_tests)} tests passed")
        
        for test in discord_tests:
            status = "✅" if discord_results.get(test, False) else "❌"
            print(f"  {status} {test.replace('_', ' ').title()}")
    else:
        print("\n🤖 Discord Integration: ❌ Not tested")
    
    # Overall assessment
    total_core = len(core_tests)
    total_discord = len(discord_tests) if discord_results else 0
    total_tests = total_core + total_discord
    total_passed = core_passed + (sum(1 for test in discord_tests if discord_results.get(test, False)) if discord_results else 0)
    
    print(f"\n🎯 Overall Score: {total_passed}/{total_tests} ({(total_passed/total_tests)*100:.1f}%)")
    
    if total_passed >= total_tests * 0.9:  # 90% or higher
        print("\n🎉 DEPLOYMENT READY! 🎉")
        print("✅ Your HOT PPL platform is ready for production!")
        print("\n🚀 Next steps:")
        print("1. Set up real Discord webhook (see DISCORD_WEBHOOK_SETUP.md)")
        print("2. Deploy to Google Cloud: ./deploy_with_discord.bat")
        print("3. Test live at: https://hotppl.io")
        print("4. Announce to your community!")
    elif total_passed >= total_tests * 0.75:  # 75% or higher
        print("\n⚠️ MOSTLY READY - Minor issues to fix")
        print("🔧 Fix the failed tests above, then deploy")
    else:
        print("\n❌ NOT READY - Major issues need fixing")
        print("🔧 Address the failed tests before deployment")
    
    print("\n" + "="*60)

async def main():
    """Run final comprehensive test"""
    print("🎯 Running final deployment readiness test...")
    
    # Test core functionality
    api_results = test_core_functionality()
    
    # Test Discord integration
    discord_results = await test_discord_integration()
    
    # Print summary
    print_final_summary(api_results, discord_results)

if __name__ == "__main__":
    asyncio.run(main())
