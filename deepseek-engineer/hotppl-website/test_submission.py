#!/usr/bin/env python3
"""
Quick test of submission API
"""

import requests
import json

def test_submission():
    """Test submission endpoint"""
    
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
            'http://localhost:8080/api/submissions',
            headers={'Content-Type': 'application/json'},
            json=submission_data
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            return response.json().get('submission_id')
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing submission...")
    submission_id = test_submission()
    if submission_id:
        print(f"✅ Submission successful! ID: {submission_id}")
    else:
        print("❌ Submission failed")
