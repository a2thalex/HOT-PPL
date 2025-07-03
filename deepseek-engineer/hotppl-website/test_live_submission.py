#!/usr/bin/env python3
"""
Test live submission API
"""

import requests
import json

def test_live_submission():
    """Test submission on live site"""
    
    submission_data = {
        "creator": "LiveTestUser",
        "scene": "THE ARRIVAL",
        "title": "Live Site Test",
        "description": "Testing submission form on live hotppl.io",
        "video_url": "https://example.com/live-test.mp4",
        "tools": "Live Testing"
    }
    
    print("🧪 Testing live submission API...")
    print(f"📝 Creator: {submission_data['creator']}")
    print(f"🎬 Scene: {submission_data['scene']}")
    
    try:
        response = requests.post(
            'https://hotppl.io/api/submissions',
            headers={'Content-Type': 'application/json'},
            json=submission_data,
            timeout=15
        )
        
        print(f"\n📤 API Response:")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Success: {data['success']}")
            print(f"🆔 Submission ID: {data['submission_id']}")
            print(f"🤖 Discord Posted: {data['discord_posted']}")
            print(f"💬 Message: {data['message']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get('https://hotppl.io/health', timeout=10)
        print(f"🔍 Health check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service: {data['service']}")
            print(f"🤖 Discord configured: {data['discord_configured']}")
            return True
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🌐 Testing Live HOT PPL Submission")
    print("=" * 40)
    
    # Test health first
    if test_health():
        print("\n" + "="*40)
        # Test submission
        success = test_live_submission()
        
        if success:
            print("\n✅ Live submission working!")
            print("🔗 Check Discord for the submission!")
        else:
            print("\n❌ Live submission failed")
    else:
        print("\n❌ Health check failed - site may be down")
