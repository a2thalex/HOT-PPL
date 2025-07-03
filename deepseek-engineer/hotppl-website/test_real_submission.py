#!/usr/bin/env python3
"""
Test submission with real Discord webhook
"""

import requests
import json

def test_real_submission():
    """Test submission with Discord posting"""
    
    submission_data = {
        "creator": "WebhookTestUser",
        "scene": "THE ARRIVAL",
        "title": "🧪 Testing Discord Integration",
        "description": "This is a test submission to verify Discord webhook integration is working perfectly!",
        "video_url": "https://example.com/webhook-test.mp4",
        "tools": "Discord Webhook, Flask API, Python"
    }
    
    print("🧪 Testing submission with real Discord webhook...")
    print(f"📝 Creator: {submission_data['creator']}")
    print(f"🎬 Scene: {submission_data['scene']}")
    print(f"📋 Title: {submission_data['title']}")
    
    try:
        response = requests.post(
            'http://localhost:8080/api/submissions',
            headers={'Content-Type': 'application/json'},
            json=submission_data,
            timeout=15
        )
        
        print(f"\n📤 API Response:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Success: {data['success']}")
            print(f"🆔 Submission ID: {data['submission_id']}")
            print(f"🤖 Discord Posted: {data['discord_posted']}")
            print(f"💬 Message: {data['message']}")
            
            if data['discord_posted']:
                print("\n🎉 SUCCESS! Check your Discord server for the new submission!")
                print("🔗 The submission should appear in #🎬-submissions channel")
                print("🔥 Community members can now vote with reactions!")
            else:
                print("\n⚠️ Submission saved but Discord posting failed")
                print("🔧 Check webhook URL and permissions")
            
            return data['submission_id']
        else:
            print(f"❌ Failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 HOT PPL Discord Integration Test")
    print("=" * 50)
    
    submission_id = test_real_submission()
    
    if submission_id:
        print(f"\n✅ Test completed successfully!")
        print(f"🎯 Submission ID: {submission_id}")
        print("\n🔍 Check your Discord server to see the submission!")
    else:
        print("\n❌ Test failed - check the errors above")
