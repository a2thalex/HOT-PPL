#!/usr/bin/env python3
"""
Test specific endpoint with detailed error info
"""

import requests
import json

def test_get_submissions():
    """Test get submissions with detailed error info"""
    
    print("🧪 Testing Get Submissions Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get('https://hotppl.io/api/submissions?status=pending', timeout=15)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {len(data['submissions'])} submissions found")
            for sub in data['submissions'][:3]:  # Show first 3
                print(f"  - {sub['creator']}: {sub['scene']} ({sub['vote_count']} votes)")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Response Text: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_leaderboard():
    """Test leaderboard with detailed error info"""
    
    print("\n🏆 Testing Leaderboard Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get('https://hotppl.io/api/leaderboard', timeout=15)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {len(data['leaderboard'])} entries found")
            for entry in data['leaderboard'][:3]:  # Show top 3
                print(f"  {entry['rank']}. {entry['creator']}: {entry['scene']} ({entry['votes']} votes)")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Response Text: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_get_submissions()
    test_leaderboard()
