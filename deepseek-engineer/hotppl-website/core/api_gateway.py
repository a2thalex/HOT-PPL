#!/usr/bin/env python3
"""
HOT PPL API Gateway
Central API layer that coordinates all platform services
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import asyncio
import threading
from datetime import datetime
import json
import os
from typing import Dict, List, Optional
import uuid

from database import db, UserRole, SubmissionStatus
# from discord_service import DiscordService
# from analytics_service import AnalyticsService
# from content_processor import ContentProcessor

# Placeholder services for now
class DiscordService:
    def is_connected(self): return True
    async def post_submission(self, submission, user): return {'message_id': '123'}

class AnalyticsService:
    def log_event(self, event, data): pass
    def get_dashboard_data(self): return {}

class ContentProcessor:
    async def analyze_submission(self, submission): return {}

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'hotppl_super_secret_2025')
CORS(app)

# Initialize services
discord_service = DiscordService()
analytics_service = AnalyticsService()
content_processor = ContentProcessor()

class APIGateway:
    def __init__(self):
        self.services = {
            'discord': discord_service,
            'analytics': analytics_service,
            'content': content_processor
        }
    
    async def process_submission(self, submission_data: Dict) -> Dict:
        """Process a new submission through all services"""
        try:
            # 1. Create user if doesn't exist
            user = db.get_user_by_discord_id(submission_data.get('discord_id', ''))
            if not user and submission_data.get('discord_id'):
                user = db.create_user(
                    discord_id=submission_data['discord_id'],
                    username=submission_data.get('username', 'Anonymous')
                )
            
            # 2. Create submission in database
            submission = db.create_submission(
                user_id=user.id if user else str(uuid.uuid4()),
                scene_name=submission_data['scene'],
                title=submission_data.get('title', f"{submission_data['scene']} Recreation"),
                description=submission_data.get('description', ''),
                video_url=submission_data['video_url'],
                tools_used=submission_data.get('tools', [])
            )
            
            # 3. Process content (async)
            content_analysis = await content_processor.analyze_submission(submission)
            
            # 4. Post to Discord
            discord_result = await discord_service.post_submission(submission, user)
            
            # 5. Log analytics
            analytics_service.log_event('submission_created', {
                'submission_id': submission.id,
                'user_id': user.id if user else None,
                'scene': submission.scene_name,
                'tools': submission.tools_used
            })
            
            return {
                'success': True,
                'submission_id': submission.id,
                'discord_message_id': discord_result.get('message_id'),
                'content_analysis': content_analysis,
                'status': 'processing'
            }
            
        except Exception as e:
            analytics_service.log_event('submission_error', {
                'error': str(e),
                'submission_data': submission_data
            })
            return {'success': False, 'error': str(e)}
    
    async def process_vote(self, vote_data: Dict) -> Dict:
        """Process a vote through all services"""
        try:
            # Update database
            # Update Discord
            # Log analytics
            # Update real-time leaderboard
            pass
        except Exception as e:
            return {'success': False, 'error': str(e)}

gateway = APIGateway()

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'database': 'connected',
            'discord': discord_service.is_connected(),
            'analytics': 'active',
            'content_processor': 'active'
        }
    })

@app.route('/api/submissions', methods=['POST'])
def create_submission():
    """Create a new submission"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['scene', 'video_url']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Process submission asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(gateway.process_submission(data))
    loop.close()
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 500

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """Get submissions with filtering and pagination"""
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    status = request.args.get('status', 'approved')
    scene = request.args.get('scene')
    
    # Get submissions from database
    # Apply filters
    # Return paginated results
    
    return jsonify({
        'submissions': [],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': 0
        }
    })

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get current leaderboard"""
    limit = int(request.args.get('limit', 10))
    leaderboard = db.get_leaderboard(limit)
    
    return jsonify({
        'leaderboard': leaderboard,
        'updated_at': datetime.now().isoformat()
    })

@app.route('/api/vote', methods=['POST'])
def cast_vote():
    """Cast a vote on a submission"""
    data = request.get_json()
    
    required_fields = ['submission_id', 'user_id', 'vote_type']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Process vote asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(gateway.process_vote(data))
    loop.close()
    
    return jsonify(result)

@app.route('/api/users/<user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    """Get user statistics"""
    user = db.get_user_by_discord_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'role': user.role.value,
        'stats': {
            'submissions': user.total_submissions,
            'votes_given': user.total_votes_given,
            'votes_received': user.total_votes_received,
            'reputation': user.reputation_score
        },
        'is_verified': user.is_verified
    })

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """Get analytics dashboard data"""
    return jsonify(analytics_service.get_dashboard_data())

@app.route('/api/discord/webhook', methods=['POST'])
def discord_webhook():
    """Handle Discord webhook events"""
    data = request.get_json()
    
    # Process Discord events
    # Update database
    # Trigger other services
    
    return jsonify({'status': 'processed'})

@app.route('/api/admin/submissions/<submission_id>/approve', methods=['POST'])
def approve_submission(submission_id):
    """Approve a submission (admin only)"""
    # Check admin permissions
    # Update submission status
    # Notify Discord
    # Update leaderboard
    
    return jsonify({'status': 'approved'})

@app.route('/api/admin/users/<user_id>/promote', methods=['POST'])
def promote_user(user_id):
    """Promote a user role (admin only)"""
    data = request.get_json()
    new_role = data.get('role')
    
    # Validate role
    # Update user
    # Update Discord roles
    # Log event
    
    return jsonify({'status': 'promoted'})

@app.route('/api/challenges', methods=['GET'])
def get_challenges():
    """Get active challenges"""
    return jsonify({
        'challenges': [],
        'active_challenge': None
    })

@app.route('/api/challenges', methods=['POST'])
def create_challenge():
    """Create a new challenge (admin only)"""
    data = request.get_json()
    
    # Create challenge
    # Announce on Discord
    # Start analytics tracking
    
    return jsonify({'status': 'created'})

# Real-time endpoints
@app.route('/api/realtime/stats', methods=['GET'])
def get_realtime_stats():
    """Get real-time platform statistics"""
    return jsonify({
        'active_users': 0,
        'submissions_today': 0,
        'votes_today': 0,
        'trending_scenes': [],
        'top_creators': []
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Background tasks
def start_background_services():
    """Start background services"""
    # Start Discord bot
    # Start analytics processor
    # Start content processor
    # Start real-time sync
    pass

if __name__ == '__main__':
    # Initialize database
    db.init_database()
    
    # Start background services
    background_thread = threading.Thread(target=start_background_services)
    background_thread.daemon = True
    background_thread.start()
    
    # Start API server
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('API_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )
