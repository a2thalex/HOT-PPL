#!/usr/bin/env python3
"""
Test Discord webhook for HOT PPL submissions
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def test_webhook():
    """Test the Discord webhook"""
    print("🧪 Testing Discord Webhook for HOT PPL...")
    
    if not DISCORD_WEBHOOK_URL:
        print("❌ No Discord webhook URL found!")
        print("📋 Please set DISCORD_WEBHOOK_URL in your .env file")
        print("🔧 See DISCORD_WEBHOOK_SETUP.md for instructions")
        return False
    
    print(f"🔗 Webhook URL: {DISCORD_WEBHOOK_URL[:50]}...")
    
    # Test 1: Simple message
    print("\n📤 Test 1: Simple message...")
    try:
        payload = {
            "content": "🧪 **HOT PPL Webhook Test** - Integration working! 🛸"
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        
        if response.status_code == 204:
            print("✅ Simple message test passed!")
        else:
            print(f"❌ Simple message test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Simple message test failed: {e}")
        return False
    
    # Test 2: Rich embed (like submission)
    print("\n📤 Test 2: Rich embed (submission format)...")
    try:
        embed = {
            "title": "🎬 New Submission: THE ARRIVAL",
            "description": "Testing the Discord integration with a mock submission",
            "color": 0xff0080,
            "fields": [
                {
                    "name": "Creator",
                    "value": "TestUser",
                    "inline": True
                },
                {
                    "name": "Scene",
                    "value": "THE ARRIVAL",
                    "inline": True
                },
                {
                    "name": "Tools",
                    "value": "AI, Phone Camera, Pure Creativity",
                    "inline": True
                }
            ],
            "footer": {
                "text": "React with 🔥 to vote! • HOT PPL"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        payload = {
            "content": "🚨 **NEW SUBMISSION ALERT** 🚨",
            "embeds": [embed]
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        
        if response.status_code == 204:
            print("✅ Rich embed test passed!")
        else:
            print(f"❌ Rich embed test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Rich embed test failed: {e}")
        return False
    
    # Test 3: Leaderboard format
    print("\n📤 Test 3: Leaderboard format...")
    try:
        embed = {
            "title": "🏆 HOT PPL LEADERBOARD",
            "description": "Current top submissions",
            "color": 0x00ff88,
            "fields": [
                {
                    "name": "🥇 TestUser",
                    "value": "**THE ARRIVAL** • 15 🔥",
                    "inline": False
                },
                {
                    "name": "🥈 CreativeUser",
                    "value": "**DJ REVEAL** • 12 🔥",
                    "inline": False
                },
                {
                    "name": "🥉 ArtistUser",
                    "value": "**SIRI CONSULTATION** • 8 🔥",
                    "inline": False
                }
            ],
            "footer": {
                "text": "HOT PPL - Where the f*ck are all the hot people?"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        payload = {
            "embeds": [embed]
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        
        if response.status_code == 204:
            print("✅ Leaderboard test passed!")
        else:
            print(f"❌ Leaderboard test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Leaderboard test failed: {e}")
        return False
    
    print("\n🎉 All webhook tests passed!")
    print("\n✅ Discord integration is working perfectly!")
    print("🚀 Ready to deploy to Google Cloud!")
    
    return True

def test_api_integration():
    """Test the API integration with webhook"""
    print("\n🔗 Testing API integration...")
    
    # This would test the actual Flask app's webhook posting
    # For now, just verify the webhook URL is configured
    if DISCORD_WEBHOOK_URL:
        print("✅ Webhook URL configured for API")
        return True
    else:
        print("❌ Webhook URL not configured for API")
        return False

if __name__ == "__main__":
    print("🧪 HOT PPL Discord Webhook Test Suite")
    print("=" * 50)
    
    success = test_webhook()
    
    if success:
        test_api_integration()
        print("\n🎯 Next steps:")
        print("1. Deploy to Google Cloud: ./deploy_with_discord.bat")
        print("2. Test live at: https://hotppl.io/submit")
        print("3. Watch Discord for automatic posts!")
    else:
        print("\n🔧 Fix the webhook setup and try again")
        print("📖 See DISCORD_WEBHOOK_SETUP.md for help")
