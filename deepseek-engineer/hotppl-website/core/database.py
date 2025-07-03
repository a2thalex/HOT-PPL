#!/usr/bin/env python3
"""
HOT PPL Core Database Architecture
Enterprise-grade database layer for the Discord-powered platform
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

class SubmissionStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FEATURED = "featured"
    ARCHIVED = "archived"

class UserRole(Enum):
    EARTHLING = "earthling"
    VERIFIED_CREATOR = "verified_creator"
    TOP_CREATOR = "top_creator"
    SCENE_MASTER = "scene_master"
    COMMUNITY_HELPER = "community_helper"
    ALIEN_ADMIN = "alien_admin"

@dataclass
class User:
    id: str
    discord_id: str
    username: str
    email: Optional[str]
    role: UserRole
    created_at: datetime
    last_active: datetime
    total_submissions: int = 0
    total_votes_given: int = 0
    total_votes_received: int = 0
    reputation_score: int = 0
    is_verified: bool = False
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

@dataclass
class Submission:
    id: str
    user_id: str
    scene_name: str
    title: str
    description: str
    video_url: str
    thumbnail_url: Optional[str]
    tools_used: List[str]
    status: SubmissionStatus
    created_at: datetime
    updated_at: datetime
    vote_count: int = 0
    view_count: int = 0
    share_count: int = 0
    discord_message_id: Optional[str] = None
    processing_data: Optional[Dict] = None

@dataclass
class Vote:
    id: str
    submission_id: str
    user_id: str
    vote_type: str  # 'fire', 'love', 'mind_blown'
    created_at: datetime
    discord_message_id: Optional[str] = None

@dataclass
class Challenge:
    id: str
    name: str
    description: str
    scenes: List[str]
    start_date: datetime
    end_date: datetime
    prize_pool: Optional[str]
    rules: Dict[str, Any]
    is_active: bool = True
    submission_count: int = 0

class HotPPLDatabase:
    def __init__(self, db_path: str = "hotppl_platform.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize all database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                discord_id TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                email TEXT,
                role TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                last_active TIMESTAMP NOT NULL,
                total_submissions INTEGER DEFAULT 0,
                total_votes_given INTEGER DEFAULT 0,
                total_votes_received INTEGER DEFAULT 0,
                reputation_score INTEGER DEFAULT 0,
                is_verified BOOLEAN DEFAULT FALSE,
                avatar_url TEXT,
                bio TEXT
            )
        ''')
        
        # Submissions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                scene_name TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                video_url TEXT NOT NULL,
                thumbnail_url TEXT,
                tools_used TEXT, -- JSON array
                status TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                vote_count INTEGER DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                share_count INTEGER DEFAULT 0,
                discord_message_id TEXT,
                processing_data TEXT, -- JSON object
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Votes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id TEXT PRIMARY KEY,
                submission_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                vote_type TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                discord_message_id TEXT,
                FOREIGN KEY (submission_id) REFERENCES submissions (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(submission_id, user_id, vote_type)
            )
        ''')
        
        # Challenges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS challenges (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                scenes TEXT, -- JSON array
                start_date TIMESTAMP NOT NULL,
                end_date TIMESTAMP NOT NULL,
                prize_pool TEXT,
                rules TEXT, -- JSON object
                is_active BOOLEAN DEFAULT TRUE,
                submission_count INTEGER DEFAULT 0
            )
        ''')
        
        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                event_data TEXT, -- JSON object
                user_id TEXT,
                submission_id TEXT,
                timestamp TIMESTAMP NOT NULL,
                discord_guild_id TEXT,
                discord_channel_id TEXT
            )
        ''')
        
        # Discord sync table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS discord_sync (
                id TEXT PRIMARY KEY,
                entity_type TEXT NOT NULL, -- 'submission', 'vote', 'user'
                entity_id TEXT NOT NULL,
                discord_message_id TEXT,
                discord_channel_id TEXT,
                sync_status TEXT NOT NULL, -- 'pending', 'synced', 'failed'
                last_sync TIMESTAMP,
                retry_count INTEGER DEFAULT 0
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_submissions_user_id ON submissions(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_submissions_created_at ON submissions(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_votes_submission_id ON votes(submission_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_votes_user_id ON votes(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_event_type ON analytics(event_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON analytics(timestamp)')
        
        conn.commit()
        conn.close()
    
    def create_user(self, discord_id: str, username: str, email: str = None) -> User:
        """Create a new user"""
        user = User(
            id=str(uuid.uuid4()),
            discord_id=discord_id,
            username=username,
            email=email,
            role=UserRole.EARTHLING,
            created_at=datetime.now(),
            last_active=datetime.now()
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (id, discord_id, username, email, role, created_at, last_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user.id, user.discord_id, user.username, user.email, 
              user.role.value, user.created_at, user.last_active))
        
        conn.commit()
        conn.close()
        
        return user
    
    def get_user_by_discord_id(self, discord_id: str) -> Optional[User]:
        """Get user by Discord ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE discord_id = ?', (discord_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0], discord_id=row[1], username=row[2], email=row[3],
                role=UserRole(row[4]), created_at=datetime.fromisoformat(row[5]),
                last_active=datetime.fromisoformat(row[6]), total_submissions=row[7],
                total_votes_given=row[8], total_votes_received=row[9],
                reputation_score=row[10], is_verified=bool(row[11]),
                avatar_url=row[12], bio=row[13]
            )
        return None
    
    def create_submission(self, user_id: str, scene_name: str, title: str, 
                         description: str, video_url: str, tools_used: List[str]) -> Submission:
        """Create a new submission"""
        submission = Submission(
            id=str(uuid.uuid4()),
            user_id=user_id,
            scene_name=scene_name,
            title=title,
            description=description,
            video_url=video_url,
            thumbnail_url=None,
            tools_used=tools_used,
            status=SubmissionStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO submissions (id, user_id, scene_name, title, description, 
                                   video_url, tools_used, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (submission.id, submission.user_id, submission.scene_name, 
              submission.title, submission.description, submission.video_url,
              json.dumps(submission.tools_used), submission.status.value,
              submission.created_at, submission.updated_at))
        
        conn.commit()
        conn.close()
        
        return submission
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get current leaderboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.*, u.username, u.avatar_url
            FROM submissions s
            JOIN users u ON s.user_id = u.id
            WHERE s.status = 'approved'
            ORDER BY s.vote_count DESC, s.created_at ASC
            LIMIT ?
        ''', (limit,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'submission_id': row[0],
                'scene_name': row[2],
                'title': row[3],
                'vote_count': row[10],
                'username': row[16],
                'avatar_url': row[17],
                'created_at': row[8]
            })
        
        conn.close()
        return results
    
    def log_analytics(self, event_type: str, event_data: Dict, 
                     user_id: str = None, submission_id: str = None):
        """Log analytics event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analytics (id, event_type, event_data, user_id, 
                                 submission_id, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (str(uuid.uuid4()), event_type, json.dumps(event_data),
              user_id, submission_id, datetime.now()))
        
        conn.commit()
        conn.close()

# Global database instance
db = HotPPLDatabase()
