#!/usr/bin/env python3
"""
Test the HOT PPL API endpoints
"""

import requests
import json
import time

BASE_URL = 'http://localhost:8080'

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f'{BASE_URL}/api/health')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_submission():
    """Test submission endpoint"""
    print("\n📤 Testing submission endpoint...")
    
    submission_data = {
        "creator": "TestUser",
        "scene": "THE ARRIVAL",
        "title": "My Test Submission",
        "description": "Testing the submission system",
        "video_url": "https://example.com/test.mp4",
        "tools": "AI, Phone Camera"
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/submissions',
            headers={'Content-Type': 'application/json'},
            json=submission_data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            return response.json().get('submission_id')
        return None
    except Exception as e:
        print(f"❌ Submission test failed: {e}")
        return None

def test_get_submissions():
    """Test get submissions endpoint"""
    print("\n📋 Testing get submissions endpoint...")
    try:
        response = requests.get(f'{BASE_URL}/api/submissions?status=pending')
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Found {len(data['submissions'])} submissions")
        for sub in data['submissions']:
            print(f"  - {sub['creator']}: {sub['scene']} ({sub['vote_count']} votes)")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Get submissions test failed: {e}")
        return False

def test_leaderboard():
    """Test leaderboard endpoint"""
    print("\n🏆 Testing leaderboard endpoint...")
    try:
        response = requests.get(f'{BASE_URL}/api/leaderboard')
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Leaderboard entries: {len(data['leaderboard'])}")
        for entry in data['leaderboard']:
            print(f"  {entry['rank']}. {entry['creator']}: {entry['scene']} ({entry['votes']} votes)")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Leaderboard test failed: {e}")
        return False

def test_voting(submission_id):
    """Test voting endpoint"""
    if not submission_id:
        print("\n⚠️ Skipping vote test - no submission ID")
        return False
    
    print(f"\n🗳️ Testing voting endpoint for submission {submission_id}...")
    
    vote_data = {
        "submission_id": submission_id,
        "voter_id": "test_voter_123"
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/vote',
            headers={'Content-Type': 'application/json'},
            json=vote_data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Voting test failed: {e}")
        return False

def test_website_access():
    """Test website pages"""
    print("\n🌐 Testing website pages...")
    
    pages = ['/', '/scenes.html', '/submit.html', '/confirmation.html']
    
    for page in pages:
        try:
            response = requests.get(f'{BASE_URL}{page}')
            status = "✅" if response.status_code == 200 else "❌"
            print(f"  {status} {page}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ {page}: {e}")

def main():
    """Run all tests"""
    print("🧪 HOT PPL API Test Suite")
    print("=" * 40)
    
    # Test health
    if not test_health():
        print("❌ Health check failed - server may not be running")
        return
    
    # Test website pages
    test_website_access()
    
    # Test submission
    submission_id = test_submission()
    
    # Test get submissions
    test_get_submissions()
    
    # Test voting
    test_voting(submission_id)
    
    # Test leaderboard
    test_leaderboard()
    
    print("\n✅ All tests completed!")
    print("\n🔗 Website available at: http://localhost:8080")
    print("📱 Try submitting through the web form at: http://localhost:8080/submit.html")

if __name__ == "__main__":
    main()
