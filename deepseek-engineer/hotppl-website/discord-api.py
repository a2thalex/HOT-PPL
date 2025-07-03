#!/usr/bin/env python3
"""
HOT PPL Discord API Integration
Connects the website with Discord for seamless community features
"""

from flask import Flask, request, jsonify, session, redirect, url_for
import requests
import os
import sqlite3
import json
from datetime import datetime, timedelta
import jwt
from functools import wraps
import asyncio
import aiohttp

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# Discord OAuth2 configuration
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI', 'https://hotppl.io/auth/discord')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

# Discord API endpoints
DISCORD_API_BASE = 'https://discord.com/api/v10'
DISCORD_OAUTH_URL = f'{DISCORD_API_BASE}/oauth2/token'
DISCORD_USER_URL = f'{DISCORD_API_BASE}/users/@me'
DISCORD_GUILD_URL = f'{DISCORD_API_BASE}/guilds/{DISCORD_GUILD_ID}'

class DiscordAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bot {DISCORD_BOT_TOKEN}',
            'Content-Type': 'application/json'
        })

    def get_guild_info(self):
        """Get Discord server information"""
        try:
            response = self.session.get(f'{DISCORD_GUILD_URL}?with_counts=true')
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting guild info: {e}")
        return None

    def send_webhook_message(self, content, embeds=None):
        """Send message via webhook"""
        if not DISCORD_WEBHOOK_URL:
            return False
        
        payload = {'content': content}
        if embeds:
            payload['embeds'] = embeds
        
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
            return response.status_code == 204
        except Exception as e:
            print(f"Error sending webhook: {e}")
            return False

    def create_submission_embed(self, submission_data):
        """Create Discord embed for new submission"""
        return {
            'title': f"🎬 New Submission: {submission_data['scene']}",
            'description': submission_data.get('description', 'No description provided'),
            'color': 0xff0080,  # Hot pink
            'fields': [
                {
                    'name': '👤 Creator',
                    'value': submission_data['creator'],
                    'inline': True
                },
                {
                    'name': '🎭 Scene',
                    'value': submission_data['scene'],
                    'inline': True
                },
                {
                    'name': '🛠️ Tools Used',
                    'value': submission_data.get('tools', 'Not specified'),
                    'inline': True
                }
            ],
            'footer': {
                'text': 'HOT PPL - Where the f*ck are all the hot people?'
            },
            'timestamp': datetime.utcnow().isoformat()
        }

discord_api = DiscordAPI()

@app.route('/api/discord/auth', methods=['POST'])
def discord_auth():
    """Handle Discord OAuth callback"""
    data = request.get_json()
    code = data.get('code')
    
    if not code:
        return jsonify({'error': 'No authorization code provided'}), 400
    
    # Exchange code for access token
    token_data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI
    }
    
    try:
        # Get access token
        token_response = requests.post(DISCORD_OAUTH_URL, data=token_data)
        token_json = token_response.json()
        
        if 'access_token' not in token_json:
            return jsonify({'error': 'Failed to get access token'}), 400
        
        access_token = token_json['access_token']
        
        # Get user info
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(DISCORD_USER_URL, headers=headers)
        user_data = user_response.json()
        
        # Store user session
        session['discord_user'] = user_data
        session['discord_token'] = access_token
        
        # Try to add user to Discord server
        try_add_to_guild(user_data['id'], access_token)
        
        return jsonify({
            'success': True,
            'user': {
                'id': user_data['id'],
                'username': user_data['username'],
                'avatar': user_data.get('avatar'),
                'discriminator': user_data.get('discriminator')
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Authentication failed: {str(e)}'}), 500

def try_add_to_guild(user_id, access_token):
    """Try to add user to Discord server"""
    if not DISCORD_GUILD_ID:
        return False
    
    url = f'{DISCORD_API_BASE}/guilds/{DISCORD_GUILD_ID}/members/{user_id}'
    data = {'access_token': access_token}
    
    try:
        response = discord_api.session.put(url, json=data)
        return response.status_code in [201, 204]  # 201 = added, 204 = already member
    except Exception as e:
        print(f"Error adding user to guild: {e}")
        return False

@app.route('/api/discord/stats', methods=['GET'])
def discord_stats():
    """Get Discord server statistics"""
    guild_info = discord_api.get_guild_info()
    
    if guild_info:
        return jsonify({
            'memberCount': guild_info.get('approximate_member_count', 0),
            'onlineCount': guild_info.get('approximate_presence_count', 0),
            'serverName': guild_info.get('name', 'HOT PPL'),
            'serverIcon': guild_info.get('icon')
        })
    
    return jsonify({'error': 'Failed to get server stats'}), 500

@app.route('/api/discord/submit', methods=['POST'])
def discord_submit():
    """Handle new submission and post to Discord"""
    data = request.get_json()
    
    # Validate submission data
    required_fields = ['creator', 'scene', 'video_url']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create Discord embed
    embed = discord_api.create_submission_embed(data)
    
    # Send to Discord
    success = discord_api.send_webhook_message(
        "🚨 **NEW SUBMISSION ALERT** 🚨",
        [embed]
    )
    
    if success:
        # Store submission in database
        store_submission(data)
        return jsonify({'success': True, 'message': 'Submission posted to Discord'})
    else:
        return jsonify({'error': 'Failed to post to Discord'}), 500

@app.route('/api/discord/vote', methods=['POST'])
def discord_vote():
    """Handle vote update from Discord"""
    data = request.get_json()
    submission_id = data.get('submission_id')
    vote_count = data.get('vote_count')
    
    if not submission_id or vote_count is None:
        return jsonify({'error': 'Missing submission_id or vote_count'}), 400
    
    # Update vote count in database
    update_vote_count(submission_id, vote_count)
    
    return jsonify({'success': True})

@app.route('/api/discord/leaderboard', methods=['GET'])
def discord_leaderboard():
    """Get current leaderboard"""
    try:
        conn = sqlite3.connect('hotppl.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, creator, scene, vote_count, submission_time
            FROM submissions
            ORDER BY vote_count DESC, submission_time ASC
            LIMIT 10
        ''')
        
        submissions = cursor.fetchall()
        conn.close()
        
        leaderboard = []
        for sub in submissions:
            leaderboard.append({
                'id': sub[0],
                'creator': sub[1],
                'scene': sub[2],
                'votes': sub[3],
                'submitted': sub[4]
            })
        
        return jsonify({'leaderboard': leaderboard})
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/discord/user/<user_id>/stats', methods=['GET'])
def user_discord_stats(user_id):
    """Get user statistics"""
    try:
        conn = sqlite3.connect('hotppl.db')
        cursor = conn.cursor()
        
        # Get submission count
        cursor.execute('SELECT COUNT(*) FROM submissions WHERE discord_user_id = ?', (user_id,))
        submission_count = cursor.fetchone()[0]
        
        # Get total votes received
        cursor.execute('''
            SELECT SUM(vote_count) FROM submissions WHERE discord_user_id = ?
        ''', (user_id,))
        votes_received = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return jsonify({
            'submissions': submission_count,
            'votes_received': votes_received,
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

def store_submission(data):
    """Store submission in database"""
    try:
        conn = sqlite3.connect('hotppl.db')
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator TEXT,
                scene TEXT,
                description TEXT,
                video_url TEXT,
                tools TEXT,
                discord_user_id TEXT,
                submission_time TIMESTAMP,
                vote_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            INSERT INTO submissions (creator, scene, description, video_url, tools, discord_user_id, submission_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['creator'],
            data['scene'],
            data.get('description', ''),
            data['video_url'],
            data.get('tools', ''),
            data.get('discord_user_id', ''),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error storing submission: {e}")

def update_vote_count(submission_id, vote_count):
    """Update vote count in database"""
    try:
        conn = sqlite3.connect('hotppl.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE submissions SET vote_count = ? WHERE id = ?
        ''', (vote_count, submission_id))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error updating vote count: {e}")

@app.route('/auth/discord')
def discord_callback():
    """Handle Discord OAuth redirect"""
    # This would typically redirect back to the frontend
    # with the auth code for the JavaScript to handle
    code = request.args.get('code')
    if code:
        return redirect(f'https://hotppl.io/?discord_code={code}')
    else:
        return redirect('https://hotppl.io/?error=discord_auth_failed')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
