#!/usr/bin/env python3
"""
HOT PPL Analytics Service
Comprehensive analytics and metrics tracking for the platform
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import uuid
from collections import defaultdict

from database import db

@dataclass
class AnalyticsEvent:
    id: str
    event_type: str
    event_data: Dict[str, Any]
    user_id: Optional[str]
    submission_id: Optional[str]
    timestamp: datetime
    discord_guild_id: Optional[str] = None
    discord_channel_id: Optional[str] = None

class AdvancedAnalyticsService:
    def __init__(self):
        self.event_types = {
            # User events
            'user_registered', 'user_login', 'user_promoted', 'user_verified',
            
            # Submission events
            'submission_created', 'submission_approved', 'submission_rejected',
            'submission_viewed', 'submission_shared', 'submission_featured',
            
            # Voting events
            'vote_cast', 'vote_removed', 'vote_changed',
            
            # Discord events
            'discord_message_sent', 'discord_reaction_added', 'discord_user_joined',
            'discord_command_used', 'discord_voice_joined',
            
            # Platform events
            'page_view', 'api_call', 'error_occurred', 'feature_used',
            
            # Challenge events
            'challenge_started', 'challenge_ended', 'challenge_participated',
            
            # Content events
            'content_processed', 'content_moderated', 'content_trending'
        }
    
    def log_event(self, event_type: str, event_data: Dict[str, Any], 
                  user_id: str = None, submission_id: str = None,
                  discord_guild_id: str = None, discord_channel_id: str = None):
        """Log an analytics event"""
        if event_type not in self.event_types:
            print(f"Warning: Unknown event type: {event_type}")
        
        event = AnalyticsEvent(
            id=str(uuid.uuid4()),
            event_type=event_type,
            event_data=event_data,
            user_id=user_id,
            submission_id=submission_id,
            timestamp=datetime.now(),
            discord_guild_id=discord_guild_id,
            discord_channel_id=discord_channel_id
        )
        
        # Store in database
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analytics (id, event_type, event_data, user_id, 
                                 submission_id, timestamp, discord_guild_id, discord_channel_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (event.id, event.event_type, json.dumps(event.event_data),
              event.user_id, event.submission_id, event.timestamp,
              event.discord_guild_id, event.discord_channel_id))
        
        conn.commit()
        conn.close()
        
        # Real-time processing
        self._process_real_time_metrics(event)
    
    def _process_real_time_metrics(self, event: AnalyticsEvent):
        """Process real-time metrics and triggers"""
        # Update real-time counters
        # Trigger notifications
        # Update leaderboards
        # Check for milestones
        pass
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard analytics"""
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        # Time ranges
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        dashboard = {
            'overview': self._get_overview_stats(cursor, today),
            'growth': self._get_growth_metrics(cursor, week_ago, month_ago),
            'engagement': self._get_engagement_metrics(cursor, today),
            'content': self._get_content_metrics(cursor, today),
            'discord': self._get_discord_metrics(cursor, today),
            'trending': self._get_trending_data(cursor),
            'real_time': self._get_real_time_stats(cursor)
        }
        
        conn.close()
        return dashboard
    
    def _get_overview_stats(self, cursor, today) -> Dict[str, Any]:
        """Get overview statistics"""
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        # Total submissions
        cursor.execute('SELECT COUNT(*) FROM submissions')
        total_submissions = cursor.fetchone()[0]
        
        # Total votes
        cursor.execute('SELECT COUNT(*) FROM votes')
        total_votes = cursor.fetchone()[0]
        
        # Active users today
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id) FROM analytics 
            WHERE timestamp >= ? AND user_id IS NOT NULL
        ''', (today,))
        active_today = cursor.fetchone()[0]
        
        # Submissions today
        cursor.execute('SELECT COUNT(*) FROM submissions WHERE created_at >= ?', (today,))
        submissions_today = cursor.fetchone()[0]
        
        return {
            'total_users': total_users,
            'total_submissions': total_submissions,
            'total_votes': total_votes,
            'active_users_today': active_today,
            'submissions_today': submissions_today
        }
    
    def _get_growth_metrics(self, cursor, week_ago, month_ago) -> Dict[str, Any]:
        """Get growth metrics"""
        # User growth
        cursor.execute('SELECT COUNT(*) FROM users WHERE created_at >= ?', (week_ago,))
        users_this_week = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE created_at >= ?', (month_ago,))
        users_this_month = cursor.fetchone()[0]
        
        # Submission growth
        cursor.execute('SELECT COUNT(*) FROM submissions WHERE created_at >= ?', (week_ago,))
        submissions_this_week = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM submissions WHERE created_at >= ?', (month_ago,))
        submissions_this_month = cursor.fetchone()[0]
        
        return {
            'users_this_week': users_this_week,
            'users_this_month': users_this_month,
            'submissions_this_week': submissions_this_week,
            'submissions_this_month': submissions_this_month
        }
    
    def _get_engagement_metrics(self, cursor, today) -> Dict[str, Any]:
        """Get engagement metrics"""
        # Average votes per submission
        cursor.execute('''
            SELECT AVG(vote_count) FROM submissions 
            WHERE status = 'approved' AND vote_count > 0
        ''')
        avg_votes = cursor.fetchone()[0] or 0
        
        # Most active users
        cursor.execute('''
            SELECT u.username, COUNT(a.id) as activity_count
            FROM users u
            JOIN analytics a ON u.id = a.user_id
            WHERE a.timestamp >= ?
            GROUP BY u.id
            ORDER BY activity_count DESC
            LIMIT 5
        ''', (today,))
        top_active_users = [{'username': row[0], 'activity': row[1]} for row in cursor.fetchall()]
        
        # Engagement rate (votes per view)
        cursor.execute('''
            SELECT 
                SUM(vote_count) as total_votes,
                SUM(view_count) as total_views
            FROM submissions 
            WHERE view_count > 0
        ''')
        votes, views = cursor.fetchone()
        engagement_rate = (votes / views * 100) if views > 0 else 0
        
        return {
            'average_votes_per_submission': round(avg_votes, 2),
            'engagement_rate_percent': round(engagement_rate, 2),
            'top_active_users': top_active_users
        }
    
    def _get_content_metrics(self, cursor, today) -> Dict[str, Any]:
        """Get content-related metrics"""
        # Popular scenes
        cursor.execute('''
            SELECT scene_name, COUNT(*) as count
            FROM submissions
            WHERE created_at >= ?
            GROUP BY scene_name
            ORDER BY count DESC
            LIMIT 5
        ''', (today - timedelta(days=7),))
        popular_scenes = [{'scene': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Popular tools
        cursor.execute('''
            SELECT tools_used FROM submissions 
            WHERE tools_used IS NOT NULL AND tools_used != '[]'
        ''')
        all_tools = []
        for row in cursor.fetchall():
            try:
                tools = json.loads(row[0])
                all_tools.extend(tools)
            except:
                continue
        
        tool_counts = defaultdict(int)
        for tool in all_tools:
            tool_counts[tool] += 1
        
        popular_tools = [{'tool': tool, 'count': count} 
                        for tool, count in sorted(tool_counts.items(), 
                                                key=lambda x: x[1], reverse=True)[:5]]
        
        # Content quality scores
        cursor.execute('''
            SELECT AVG(vote_count), AVG(view_count), AVG(share_count)
            FROM submissions 
            WHERE status = 'approved'
        ''')
        avg_votes, avg_views, avg_shares = cursor.fetchone()
        
        return {
            'popular_scenes': popular_scenes,
            'popular_tools': popular_tools,
            'average_quality_scores': {
                'votes': round(avg_votes or 0, 2),
                'views': round(avg_views or 0, 2),
                'shares': round(avg_shares or 0, 2)
            }
        }
    
    def _get_discord_metrics(self, cursor, today) -> Dict[str, Any]:
        """Get Discord-specific metrics"""
        # Discord activity
        cursor.execute('''
            SELECT COUNT(*) FROM analytics 
            WHERE event_type LIKE 'discord_%' AND timestamp >= ?
        ''', (today,))
        discord_activity_today = cursor.fetchone()[0]
        
        # Most used Discord commands
        cursor.execute('''
            SELECT event_data FROM analytics 
            WHERE event_type = 'discord_command_used' AND timestamp >= ?
        ''', (today - timedelta(days=7),))
        
        command_counts = defaultdict(int)
        for row in cursor.fetchall():
            try:
                data = json.loads(row[0])
                command = data.get('command', 'unknown')
                command_counts[command] += 1
            except:
                continue
        
        popular_commands = [{'command': cmd, 'count': count} 
                           for cmd, count in sorted(command_counts.items(), 
                                                  key=lambda x: x[1], reverse=True)[:5]]
        
        return {
            'discord_activity_today': discord_activity_today,
            'popular_commands': popular_commands
        }
    
    def _get_trending_data(self, cursor) -> Dict[str, Any]:
        """Get trending content and creators"""
        # Trending submissions (high vote velocity)
        cursor.execute('''
            SELECT s.id, s.title, s.scene_name, s.vote_count, u.username
            FROM submissions s
            JOIN users u ON s.user_id = u.id
            WHERE s.created_at >= ? AND s.status = 'approved'
            ORDER BY (s.vote_count / (julianday('now') - julianday(s.created_at))) DESC
            LIMIT 5
        ''', (datetime.now() - timedelta(days=3),))
        
        trending_submissions = []
        for row in cursor.fetchall():
            trending_submissions.append({
                'id': row[0],
                'title': row[1],
                'scene': row[2],
                'votes': row[3],
                'creator': row[4]
            })
        
        # Rising creators (recent high activity)
        cursor.execute('''
            SELECT u.username, COUNT(s.id) as recent_submissions, SUM(s.vote_count) as total_votes
            FROM users u
            JOIN submissions s ON u.id = s.user_id
            WHERE s.created_at >= ? AND s.status = 'approved'
            GROUP BY u.id
            ORDER BY (COUNT(s.id) + SUM(s.vote_count)) DESC
            LIMIT 5
        ''', (datetime.now() - timedelta(days=7),))
        
        rising_creators = []
        for row in cursor.fetchall():
            rising_creators.append({
                'username': row[0],
                'recent_submissions': row[1],
                'total_votes': row[2]
            })
        
        return {
            'trending_submissions': trending_submissions,
            'rising_creators': rising_creators
        }
    
    def _get_real_time_stats(self, cursor) -> Dict[str, Any]:
        """Get real-time statistics"""
        # Activity in last hour
        hour_ago = datetime.now() - timedelta(hours=1)
        
        cursor.execute('''
            SELECT COUNT(*) FROM analytics WHERE timestamp >= ?
        ''', (hour_ago,))
        activity_last_hour = cursor.fetchone()[0]
        
        # Recent events
        cursor.execute('''
            SELECT event_type, COUNT(*) as count
            FROM analytics 
            WHERE timestamp >= ?
            GROUP BY event_type
            ORDER BY count DESC
            LIMIT 10
        ''', (hour_ago,))
        
        recent_events = [{'event': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        return {
            'activity_last_hour': activity_last_hour,
            'recent_events': recent_events,
            'last_updated': datetime.now().isoformat()
        }
    
    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get analytics for a specific user"""
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        # User activity timeline
        cursor.execute('''
            SELECT event_type, timestamp, event_data
            FROM analytics 
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 50
        ''', (user_id,))
        
        activity_timeline = []
        for row in cursor.fetchall():
            activity_timeline.append({
                'event': row[0],
                'timestamp': row[1],
                'data': json.loads(row[2]) if row[2] else {}
            })
        
        conn.close()
        
        return {
            'activity_timeline': activity_timeline
        }

# Global analytics service instance
analytics_service = AdvancedAnalyticsService()
