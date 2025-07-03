#!/usr/bin/env python3

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configure client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def test_api():
    """Test the DeepSeek API connection and model availability"""
    print("🧪 Testing DeepSeek API connection...")
    
    try:
        # Test with deepseek-chat model (more widely available)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Can you confirm you're working?"}
            ],
            max_tokens=100
        )
        
        print("✅ API connection successful!")
        print(f"📝 Response: {response.choices[0].message.content}")
        
        # Test if deepseek-reasoner is available
        try:
            reasoner_response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Test message"}
                ],
                max_tokens=50
            )
            print("✅ deepseek-reasoner model is available!")
        except Exception as e:
            print(f"⚠️ deepseek-reasoner not available: {e}")
            print("📝 Will use deepseek-chat as fallback")
        
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

if __name__ == "__main__":
    test_api()
