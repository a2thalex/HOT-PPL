#!/usr/bin/env python3
"""
Complete End-to-End Test for HOT PPL Discord Integration
Tests everything: Discord bot, website API, database, webhooks, voting
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

class SystemTester:
    def __init__(self):
        self.test_results = {}
        self.discord_client = None
        self.test_submission_id = None
        
    def log_test(self, test_name, success, message=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results[test_name] = {'success': success, 'message': message}
        
    def test_database(self):
        """Test database functionality"""
        print("\n🗄️ Testing Database...")
        
        try:
            # Test database connection
            conn = sqlite3.connect('hotppl_platform.db')
            cursor = conn.cursor()
            
            # Test tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['submissions', 'votes', 'user_stats']
            for table in required_tables:
                if table in tables:
                    self.log_test(f"Database table '{table}'", True, "exists")
                else:
                    self.log_test(f"Database table '{table}'", False, "missing")
                    
            # Test insert/query
            cursor.execute('''
                INSERT OR REPLACE INTO submissions 
                (id, creator, scene, title, description, video_url, submission_time, vote_count, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('test-123', 'TestUser', 'THE ARRIVAL', 'Test Submission', 
                  'Testing database', 'http://test.com/video.mp4', 
                  datetime.now().isoformat(), 0, 'pending'))
            
            conn.commit()
            
            # Test query
            cursor.execute('SELECT * FROM submissions WHERE id = ?', ('test-123',))
            result = cursor.fetchone()
            
            if result:
                self.log_test("Database insert/query", True, "data persisted correctly")
                self.test_submission_id = 'test-123'
            else:
                self.log_test("Database insert/query", False, "data not found")
                
            conn.close()
            
        except Exception as e:
            self.log_test("Database connection", False, str(e))
    
    def test_api_endpoints(self):
        """Test all API endpoints"""
        print("\n🌐 Testing API Endpoints...")
        
        # Test health endpoint
        try:
            response = requests.get(f'{API_BASE}/health', timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("API health endpoint", True, f"status: {data.get('status')}")
            else:
                self.log_test("API health endpoint", False, f"status code: {response.status_code}")
        except Exception as e:
            self.log_test("API health endpoint", False, str(e))
        
        # Test submission endpoint
        try:
            submission_data = {
                "creator": "APITestUser",
                "scene": "DJ REVEAL",
                "title": "API Test Submission",
                "description": "Testing the submission API endpoint",
                "video_url": "https://example.com/test-video.mp4",
                "tools": "Python, API Testing"
            }
            
            response = requests.post(
                f'{API_BASE}/api/submissions',
                headers={'Content-Type': 'application/json'},
                json=submission_data,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.log_test("API submission endpoint", True, f"ID: {data.get('submission_id')}")
                if data.get('submission_id'):
                    self.test_submission_id = data['submission_id']
            else:
                self.log_test("API submission endpoint", False, f"status: {response.status_code}")
                
        except Exception as e:
            self.log_test("API submission endpoint", False, str(e))
        
        # Test get submissions endpoint
        try:
            response = requests.get(f'{API_BASE}/api/submissions?status=pending', timeout=5)
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('submissions', []))
                self.log_test("API get submissions", True, f"found {count} submissions")
            else:
                self.log_test("API get submissions", False, f"status: {response.status_code}")
        except Exception as e:
            self.log_test("API get submissions", False, str(e))
        
        # Test leaderboard endpoint
        try:
            response = requests.get(f'{API_BASE}/api/leaderboard', timeout=5)
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('leaderboard', []))
                self.log_test("API leaderboard", True, f"found {count} entries")
            else:
                self.log_test("API leaderboard", False, f"status: {response.status_code}")
        except Exception as e:
            self.log_test("API leaderboard", False, str(e))
        
        # Test voting endpoint
        if self.test_submission_id:
            try:
                vote_data = {
                    "submission_id": self.test_submission_id,
                    "voter_id": "test-voter-123"
                }
                
                response = requests.post(
                    f'{API_BASE}/api/vote',
                    headers={'Content-Type': 'application/json'},
                    json=vote_data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    self.log_test("API voting endpoint", True, "vote cast successfully")
                else:
                    self.log_test("API voting endpoint", False, f"status: {response.status_code}")
            except Exception as e:
                self.log_test("API voting endpoint", False, str(e))
    
    def test_webhook(self):
        """Test Discord webhook"""
        print("\n🪝 Testing Discord Webhook...")
        
        if not DISCORD_WEBHOOK_URL:
            self.log_test("Discord webhook", False, "webhook URL not configured")
            return
        
        try:
            # Test simple message
            payload = {
                "content": "🧪 **System Test** - Webhook integration working!"
            }
            
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
            
            if response.status_code == 204:
                self.log_test("Discord webhook simple", True, "message sent")
            else:
                self.log_test("Discord webhook simple", False, f"status: {response.status_code}")
            
            # Test rich embed
            embed = {
                "title": "🧪 System Test Submission",
                "description": "Testing complete Discord integration",
                "color": 0xff0080,
                "fields": [
                    {"name": "Creator", "value": "SystemTester", "inline": True},
                    {"name": "Scene", "value": "SYSTEM TEST", "inline": True},
                    {"name": "Status", "value": "✅ All systems operational", "inline": True}
                ],
                "footer": {"text": "HOT PPL System Test"},
                "timestamp": datetime.now().isoformat()
            }
            
            payload = {
                "content": "🚨 **SYSTEM TEST ALERT** 🚨",
                "embeds": [embed]
            }
            
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
            
            if response.status_code == 204:
                self.log_test("Discord webhook embed", True, "rich embed sent")
            else:
                self.log_test("Discord webhook embed", False, f"status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Discord webhook", False, str(e))
    
    async def test_discord_bot(self):
        """Test Discord bot functionality"""
        print("\n🤖 Testing Discord Bot...")
        
        if not DISCORD_BOT_TOKEN:
            self.log_test("Discord bot", False, "bot token not configured")
            return
        
        try:
            # Create Discord client
            intents = discord.Intents.default()
            intents.guilds = True
            intents.reactions = True
            self.discord_client = discord.Client(intents=intents)
            
            @self.discord_client.event
            async def on_ready():
                try:
                    self.log_test("Discord bot connection", True, f"connected as {self.discord_client.user}")
                    
                    # Test guild access
                    guild = self.discord_client.get_guild(DISCORD_GUILD_ID)
                    if guild:
                        self.log_test("Discord guild access", True, f"found {guild.name}")
                        
                        # Test channel access
                        submission_channel = guild.get_channel(SUBMISSION_CHANNEL_ID)
                        voting_channel = guild.get_channel(VOTING_CHANNEL_ID)
                        leaderboard_channel = guild.get_channel(LEADERBOARD_CHANNEL_ID)
                        
                        channels_found = 0
                        if submission_channel:
                            self.log_test("Submission channel", True, f"#{submission_channel.name}")
                            channels_found += 1
                        else:
                            self.log_test("Submission channel", False, "not found")
                            
                        if voting_channel:
                            self.log_test("Voting channel", True, f"#{voting_channel.name}")
                            channels_found += 1
                        else:
                            self.log_test("Voting channel", False, "not found")
                            
                        if leaderboard_channel:
                            self.log_test("Leaderboard channel", True, f"#{leaderboard_channel.name}")
                            channels_found += 1
                        else:
                            self.log_test("Leaderboard channel", False, "not found")
                        
                        # Test posting to submission channel
                        if submission_channel:
                            try:
                                embed = discord.Embed(
                                    title="🧪 Bot Test Message",
                                    description="Testing Discord bot posting capability",
                                    color=0x00ff88
                                )
                                embed.add_field(name="Test Status", value="✅ Bot is working", inline=False)
                                embed.set_footer(text="HOT PPL System Test")
                                
                                message = await submission_channel.send(embed=embed)
                                await message.add_reaction('🔥')
                                
                                self.log_test("Discord bot posting", True, "message posted with reaction")
                                
                            except Exception as e:
                                self.log_test("Discord bot posting", False, str(e))
                        
                    else:
                        self.log_test("Discord guild access", False, f"guild {DISCORD_GUILD_ID} not found")
                    
                except Exception as e:
                    self.log_test("Discord bot testing", False, str(e))
                finally:
                    await self.discord_client.close()
            
            # Connect with timeout
            await asyncio.wait_for(self.discord_client.start(DISCORD_BOT_TOKEN), timeout=30)
            
        except asyncio.TimeoutError:
            self.log_test("Discord bot", False, "connection timeout")
        except Exception as e:
            self.log_test("Discord bot", False, str(e))
    
    def test_website_pages(self):
        """Test website accessibility"""
        print("\n🌐 Testing Website Pages...")
        
        pages = {
            '/': 'Main page',
            '/scenes.html': 'Scenes page',
            '/submit.html': 'Submit page',
            '/confirmation.html': 'Confirmation page'
        }
        
        for path, name in pages.items():
            try:
                response = requests.get(f'{API_BASE}{path}', timeout=5)
                if response.status_code == 200:
                    self.log_test(f"Website {name}", True, "accessible")
                else:
                    self.log_test(f"Website {name}", False, f"status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Website {name}", False, str(e))
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("🧪 HOT PPL SYSTEM TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\n📊 Results: {passed_tests}/{total_tests} tests passed")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests ({failed_tests}):")
            for test_name, result in self.test_results.items():
                if not result['success']:
                    print(f"  • {test_name}: {result['message']}")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! 🎉")
            print("✅ Your HOT PPL Discord integration is fully functional!")
            print("\n🚀 Ready for deployment:")
            print("1. Set up Discord webhook (see DISCORD_WEBHOOK_SETUP.md)")
            print("2. Deploy: ./deploy_with_discord.bat")
            print("3. Go live: https://hotppl.io")
        else:
            print(f"\n⚠️ {failed_tests} issues need to be fixed before deployment")
            print("🔧 Check the failed tests above and resolve them")
        
        print("\n" + "="*60)

async def main():
    """Run complete system test"""
    print("🧪 HOT PPL COMPLETE SYSTEM TEST")
    print("Testing Discord integration, API, database, and website...")
    print("="*60)
    
    tester = SystemTester()
    
    # Run all tests
    tester.test_database()
    tester.test_api_endpoints()
    tester.test_webhook()
    await tester.test_discord_bot()
    tester.test_website_pages()
    
    # Print summary
    tester.print_summary()

if __name__ == "__main__":
    asyncio.run(main())
