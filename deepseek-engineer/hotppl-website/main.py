# main.py - App Engine entry point for HOT PPL platform
# This file serves both static content and API endpoints with Discord integration

from flask import Flask, request, jsonify, send_from_directory
import os
import asyncio
import discord
from datetime import datetime
from dotenv import load_dotenv
import json
import uuid
import logging
from google.cloud import datastore

# Configure logging for App Engine
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables (for local development)
load_dotenv()

app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'hotppl_secret_key')

# Discord configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', '0'))
SUBMISSION_CHANNEL_ID = int(os.getenv('SUBMISSION_CHANNEL_ID', '0'))
VOTING_CHANNEL_ID = int(os.getenv('VOTING_CHANNEL_ID', '0'))
LEADERBOARD_CHANNEL_ID = int(os.getenv('LEADERBOARD_CHANNEL_ID', '0'))

# Initialize Datastore
def init_database():
    """Initialize Datastore database"""
    try:
        global db
        db = datastore.Client()
        logger.info("Datastore database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Datastore initialization failed: {e}")
        return False

# Global database instance
db = None

# Discord webhook for posting (simpler than full bot for App Engine)
async def post_to_discord_webhook(submission_data):
    """Post submission to Discord via webhook"""
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        logger.warning("No Discord webhook URL configured")
        return None

    try:
        import aiohttp

        embed = {
            "title": f"🎬 New Submission: {submission_data['scene']}",
            "description": submission_data.get('description', ''),
            "color": 0xff0080,
            "fields": [
                {"name": "Creator", "value": submission_data['creator'], "inline": True},
                {"name": "Scene", "value": submission_data['scene'], "inline": True},
                {"name": "Tools", "value": submission_data.get('tools', 'Not specified'), "inline": True}
            ],
            "footer": {"text": "React with 🔥 to vote! • HOT PPL"},
            "timestamp": datetime.now().isoformat()
        }

        payload = {
            "content": "🚨 **NEW SUBMISSION ALERT** 🚨",
            "embeds": [embed]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 204:
                    logger.info("Successfully posted to Discord")
                    return True
                else:
                    logger.error(f"Discord webhook failed: {response.status}")
                    return False

    except Exception as e:
        logger.error(f"Failed to post to Discord: {e}")
        return False

# Routes
@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('public', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    try:
        return send_from_directory('public', filename)
    except:
        # If file not found, serve index.html for SPA routing
        return send_from_directory('public', 'index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'hotppl-website',
        'timestamp': datetime.now().isoformat(),
        'discord_configured': bool(DISCORD_BOT_TOKEN),
        'environment': os.getenv('ENVIRONMENT', 'development')
    }), 200

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'website': 'HOT PPL',
        'status': 'live',
        'message': 'Where the f*ck are all the hot people?',
        'api_version': '1.0',
        'features': ['submissions', 'voting', 'leaderboard', 'discord_integration']
    }), 200

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

        # Store in Datastore
        key = db.key('Submission', submission_id)
        entity = datastore.Entity(key=key)
        entity.update({
            'id': submission_id,
            'creator': data['creator'],
            'scene': data['scene'],
            'title': data.get('title', f"{data['scene']} Recreation"),
            'description': data.get('description', ''),
            'video_url': data['video_url'],
            'tools': data.get('tools', ''),
            'submission_time': datetime.now(),
            'vote_count': 0,
            'status': 'pending',
            'discord_message_id': None
        })

        db.put(entity)

        # Post to Discord (async)
        discord_posted = False
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            discord_posted = loop.run_until_complete(post_to_discord_webhook(data))
            loop.close()
        except Exception as e:
            logger.error(f"Discord posting failed: {e}")

        logger.info(f"New submission created: {submission_id} by {data['creator']}")

        return jsonify({
            'success': True,
            'submission_id': submission_id,
            'discord_posted': discord_posted,
            'message': 'Submission received successfully!'
        }), 201

    except Exception as e:
        logger.error(f"Submission creation failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """Get submissions with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        status = request.args.get('status', 'pending')  # Changed default to pending

        # Simple query without complex ordering (fallback while indexes build)
        query = db.query(kind='Submission')
        query.add_filter('status', '=', status)
        entities = list(query.fetch())

        # Sort in Python (more reliable while indexes are building)
        entities.sort(key=lambda x: (-x.get('vote_count', 0), x.get('submission_time', datetime.min)))

        submissions = []
        for entity in entities:
            submissions.append({
                'id': entity.get('id', ''),
                'creator': entity.get('creator', ''),
                'scene': entity.get('scene', ''),
                'title': entity.get('title', ''),
                'description': entity.get('description', ''),
                'vote_count': entity.get('vote_count', 0),
                'submission_time': entity['submission_time'].isoformat() if hasattr(entity.get('submission_time'), 'isoformat') else str(entity.get('submission_time', ''))
            })

        total = len(submissions)

        # Simple pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_submissions = submissions[start_idx:end_idx]

        return jsonify({
            'submissions': paginated_submissions,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit if total > 0 else 0
            }
        })

    except Exception as e:
        logger.error(f"Get submissions failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/leaderboard')
def get_leaderboard():
    """Get current leaderboard"""
    try:
        limit = int(request.args.get('limit', 10))

        # Simple query for leaderboard (fallback while indexes build)
        query = db.query(kind='Submission')
        query.add_filter('status', '=', 'pending')
        entities = list(query.fetch())

        # Sort in Python and limit
        entities.sort(key=lambda x: (-x.get('vote_count', 0), x.get('submission_time', datetime.min)))
        entities = entities[:limit]

        leaderboard = []
        for i, entity in enumerate(entities, 1):
            leaderboard.append({
                'rank': i,
                'creator': entity.get('creator', ''),
                'scene': entity.get('scene', ''),
                'votes': entity.get('vote_count', 0),
                'submission_time': entity['submission_time'].isoformat() if hasattr(entity.get('submission_time'), 'isoformat') else str(entity.get('submission_time', ''))
            })

        return jsonify({
            'leaderboard': leaderboard,
            'updated_at': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Get leaderboard failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/vote', methods=['POST'])
def cast_vote():
    """Cast a vote on a submission"""
    try:
        data = request.get_json()

        required_fields = ['submission_id', 'voter_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        submission_id = data['submission_id']
        voter_id = data['voter_id']

        # Check if user already voted (simplified query)
        vote_query = db.query(kind='Vote')
        vote_query.add_filter('submission_id', '=', submission_id)
        all_votes = list(vote_query.fetch())
        existing_votes = [v for v in all_votes if v.get('voter_id') == voter_id]

        if existing_votes:
            return jsonify({'error': 'Already voted'}), 400

        # Add vote
        vote_key = db.key('Vote')
        vote_entity = datastore.Entity(key=vote_key)
        vote_entity.update({
            'submission_id': submission_id,
            'voter_id': voter_id,
            'vote_time': datetime.now()
        })
        db.put(vote_entity)

        # Update vote count
        submission_key = db.key('Submission', submission_id)
        submission_entity = db.get(submission_key)
        if submission_entity:
            submission_entity['vote_count'] += 1
            db.put(submission_entity)

        logger.info(f"Vote cast: {data['voter_id']} -> {data['submission_id']}")

        return jsonify({'success': True, 'message': 'Vote cast successfully'})

    except Exception as e:
        logger.error(f"Vote casting failed: {e}")
        return jsonify({'error': str(e)}), 500

# Initialize database on startup
init_database()

if __name__ == '__main__':
    # This is used when running locally only
    app.run(debug=True, host='0.0.0.0', port=8080)
