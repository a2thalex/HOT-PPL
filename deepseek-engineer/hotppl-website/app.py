#!/usr/bin/env python3
"""
HOT PPL Flask Application - Main web server with Discord integration
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import sqlite3
import asyncio
import discord
from datetime import datetime
from dotenv import load_dotenv
import json
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'hotppl_secret_key')

# Discord configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', '0'))
SUBMISSION_CHANNEL_ID = int(os.getenv('SUBMISSION_CHANNEL_ID', '0'))
VOTING_CHANNEL_ID = int(os.getenv('VOTING_CHANNEL_ID', '0'))
LEADERBOARD_CHANNEL_ID = int(os.getenv('LEADERBOARD_CHANNEL_ID', '0'))

# Initialize database
def init_database():
    """Initialize the database"""
    conn = sqlite3.connect('hotppl_platform.db')
    cursor = conn.cursor()
    
    # Submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator TEXT,
            scene TEXT,
            title TEXT,
            description TEXT,
            video_url TEXT,
            tools TEXT,
            discord_user_id TEXT,
            submission_time TIMESTAMP,
            vote_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            discord_message_id TEXT
        )
    ''')
    
    # Votes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER,
            voter_id TEXT,
            vote_time TIMESTAMP,
            FOREIGN KEY (submission_id) REFERENCES submissions (id),
            UNIQUE(submission_id, voter_id)
        )
    ''')
    
    # User stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            submissions_count INTEGER DEFAULT 0,
            votes_given INTEGER DEFAULT 0,
            votes_received INTEGER DEFAULT 0,
            join_date TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Discord client for posting messages
discord_client = None

async def init_discord():
    """Initialize Discord client"""
    global discord_client
    if not DISCORD_BOT_TOKEN:
        return False
    
    try:
        intents = discord.Intents.default()
        intents.guilds = True
        discord_client = discord.Client(intents=intents)
        
        @discord_client.event
        async def on_ready():
            print(f"✅ Discord client connected as {discord_client.user}")
        
        await discord_client.login(DISCORD_BOT_TOKEN)
        return True
    except Exception as e:
        print(f"❌ Discord connection failed: {e}")
        return False

async def post_to_discord(submission_data):
    """Post submission to Discord"""
    if not discord_client:
        return None
    
    try:
        channel = discord_client.get_channel(SUBMISSION_CHANNEL_ID)
        if not channel:
            return None
        
        embed = discord.Embed(
            title=f"🎬 New Submission: {submission_data['scene']}",
            description=submission_data.get('description', ''),
            color=0xff0080
        )
        embed.add_field(name="Creator", value=submission_data['creator'], inline=True)
        embed.add_field(name="Scene", value=submission_data['scene'], inline=True)
        embed.add_field(name="Tools", value=submission_data.get('tools', 'Not specified'), inline=True)
        embed.set_footer(text="React with 🔥 to vote! • HOT PPL")
        embed.timestamp = datetime.now()
        
        message = await channel.send(embed=embed)
        await message.add_reaction('🔥')
        
        return message.id
    except Exception as e:
        print(f"❌ Failed to post to Discord: {e}")
        return None

# Routes
@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('public', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('public', filename)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'hotppl-website',
        'timestamp': datetime.now().isoformat(),
        'discord_connected': discord_client is not None
    })

@app.route('/api/submissions', methods=['POST'])
def create_submission():
    """Handle new submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['creator', 'scene', 'video_url']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate submission ID
        submission_id = str(uuid.uuid4())
        
        # Store in database
        conn = sqlite3.connect('hotppl_platform.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO submissions (id, creator, scene, title, description, video_url, tools, submission_time, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            submission_id,
            data['creator'],
            data['scene'],
            data.get('title', f"{data['scene']} Recreation"),
            data.get('description', ''),
            data['video_url'],
            data.get('tools', ''),
            datetime.now(),
            'pending'
        ))
        
        conn.commit()
        conn.close()
        
        # Post to Discord (if available)
        discord_message_id = None
        if discord_client:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            discord_message_id = loop.run_until_complete(post_to_discord(data))
            loop.close()
        
        # Update with Discord message ID
        if discord_message_id:
            conn = sqlite3.connect('hotppl_platform.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE submissions SET discord_message_id = ? WHERE id = ?', 
                          (discord_message_id, submission_id))
            conn.commit()
            conn.close()
        
        return jsonify({
            'success': True,
            'submission_id': submission_id,
            'discord_posted': discord_message_id is not None,
            'message': 'Submission received successfully!'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """Get submissions with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        status = request.args.get('status', 'approved')
        
        offset = (page - 1) * limit
        
        conn = sqlite3.connect('hotppl_platform.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, creator, scene, title, description, vote_count, submission_time
            FROM submissions
            WHERE status = ?
            ORDER BY vote_count DESC, submission_time DESC
            LIMIT ? OFFSET ?
        ''', (status, limit, offset))
        
        submissions = []
        for row in cursor.fetchall():
            submissions.append({
                'id': row[0],
                'creator': row[1],
                'scene': row[2],
                'title': row[3],
                'description': row[4],
                'vote_count': row[5],
                'submission_time': row[6]
            })
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM submissions WHERE status = ?', (status,))
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'submissions': submissions,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leaderboard')
def get_leaderboard():
    """Get current leaderboard"""
    try:
        limit = int(request.args.get('limit', 10))
        
        conn = sqlite3.connect('hotppl_platform.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT creator, scene, vote_count, submission_time
            FROM submissions
            WHERE status = 'approved'
            ORDER BY vote_count DESC, submission_time ASC
            LIMIT ?
        ''', (limit,))
        
        leaderboard = []
        for i, row in enumerate(cursor.fetchall(), 1):
            leaderboard.append({
                'rank': i,
                'creator': row[0],
                'scene': row[1],
                'votes': row[2],
                'submission_time': row[3]
            })
        
        conn.close()
        
        return jsonify({
            'leaderboard': leaderboard,
            'updated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vote', methods=['POST'])
def cast_vote():
    """Cast a vote on a submission"""
    try:
        data = request.get_json()
        
        required_fields = ['submission_id', 'voter_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = sqlite3.connect('hotppl_platform.db')
        cursor = conn.cursor()
        
        # Check if user already voted
        cursor.execute('SELECT id FROM votes WHERE submission_id = ? AND voter_id = ?',
                      (data['submission_id'], data['voter_id']))
        
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Already voted'}), 400
        
        # Add vote
        cursor.execute('''
            INSERT INTO votes (submission_id, voter_id, vote_time)
            VALUES (?, ?, ?)
        ''', (data['submission_id'], data['voter_id'], datetime.now()))
        
        # Update vote count
        cursor.execute('''
            UPDATE submissions SET vote_count = vote_count + 1 WHERE id = ?
        ''', (data['submission_id'],))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Vote cast successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Initialize Discord (optional)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(init_discord())
        loop.close()
    except Exception as e:
        print(f"⚠️ Discord initialization failed: {e}")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=8080)
