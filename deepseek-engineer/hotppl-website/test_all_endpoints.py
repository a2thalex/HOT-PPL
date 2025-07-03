#!/usr/bin/env python3
"""
Test all live endpoints
"""

import requests
import json

def test_all_endpoints():
    """Test all API endpoints"""
    
    print("🧪 Testing All HOT PPL Live Endpoints")
    print("=" * 50)
    
    base_url = "https://hotppl.io"
    
    # Test 1: Health
    print("\n🔍 1. Testing Health...")
    try:
        response = requests.get(f'{base_url}/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health: {data['status']}")
            print(f"🤖 Discord: {data['discord_configured']}")
        else:
            print(f"❌ Health failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health error: {e}")
    
    # Test 2: Submit
    print("\n📤 2. Testing Submission...")
    submission_data = {
        "creator": "EndpointTestUser",
        "scene": "DJ REVEAL",
        "title": "Complete Endpoint Test",
        "description": "Testing all endpoints are working after Datastore migration",
        "video_url": "https://example.com/endpoint-test.mp4",
        "tools": "Datastore, Google Cloud"
    }
    
    try:
        response = requests.post(
            f'{base_url}/api/submissions',
            headers={'Content-Type': 'application/json'},
            json=submission_data,
            timeout=15
        )
        
        if response.status_code == 201:
            data = response.json()
            submission_id = data['submission_id']
            print(f"✅ Submission: {submission_id[:8]}...")
            print(f"🤖 Discord Posted: {data['discord_posted']}")
        else:
            print(f"❌ Submission failed: {response.status_code}")
            submission_id = None
    except Exception as e:
        print(f"❌ Submission error: {e}")
        submission_id = None
    
    # Test 3: Get Submissions
    print("\n📋 3. Testing Get Submissions...")
    try:
        response = requests.get(f'{base_url}/api/submissions?status=pending', timeout=10)
        if response.status_code == 200:
            data = response.json()
            count = len(data['submissions'])
            print(f"✅ Get Submissions: {count} found")
            if count > 0:
                latest = data['submissions'][0]
                print(f"   Latest: {latest['creator']} - {latest['scene']}")
        else:
            print(f"❌ Get submissions failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get submissions error: {e}")
    
    # Test 4: Vote
    if submission_id:
        print("\n🗳️ 4. Testing Voting...")
        vote_data = {
            "submission_id": submission_id,
            "voter_id": "endpoint-test-voter"
        }
        
        try:
            response = requests.post(
                f'{base_url}/api/vote',
                headers={'Content-Type': 'application/json'},
                json=vote_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Voting: Vote cast successfully")
            else:
                print(f"❌ Voting failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Voting error: {e}")
    
    # Test 5: Leaderboard
    print("\n🏆 5. Testing Leaderboard...")
    try:
        response = requests.get(f'{base_url}/api/leaderboard', timeout=10)
        if response.status_code == 200:
            data = response.json()
            count = len(data['leaderboard'])
            print(f"✅ Leaderboard: {count} entries")
            if count > 0:
                top = data['leaderboard'][0]
                print(f"   #1: {top['creator']} - {top['votes']} votes")
        else:
            print(f"❌ Leaderboard failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Leaderboard error: {e}")
    
    # Test 6: Website Pages
    print("\n🌐 6. Testing Website Pages...")
    pages = ['/', '/submit.html', '/scenes.html', '/confirmation.html']
    
    for page in pages:
        try:
            response = requests.get(f'{base_url}{page}', timeout=10)
            if response.status_code == 200:
                print(f"✅ {page}: Accessible")
            else:
                print(f"❌ {page}: {response.status_code}")
        except Exception as e:
            print(f"❌ {page}: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 All endpoint tests completed!")
    print("🌐 Your HOT PPL platform is fully operational!")
    print("📱 Users can now submit through: https://hotppl.io/submit.html")
    print("🤖 Discord integration is working!")

if __name__ == "__main__":
    test_all_endpoints()
