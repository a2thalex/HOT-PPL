#!/usr/bin/env python3
"""
HOT PPL Real-Time Sync Engine
Advanced bidirectional synchronization between website and Discord
"""

import asyncio
import websockets
import json
import redis
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
import uuid
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import time

from database import db
from discord_service import discord_service
from analytics_service import analytics_service

class SyncEventType(Enum):
    SUBMISSION_CREATED = "submission_created"
    VOTE_CAST = "vote_cast"
    VOTE_REMOVED = "vote_removed"
    LEADERBOARD_UPDATED = "leaderboard_updated"
    USER_JOINED = "user_joined"
    USER_PROMOTED = "user_promoted"
    CHALLENGE_STARTED = "challenge_started"
    TRENDING_UPDATED = "trending_updated"
    LIVE_STATS_UPDATED = "live_stats_updated"

@dataclass
class SyncEvent:
    id: str
    event_type: SyncEventType
    data: Dict[str, Any]
    source: str  # 'website', 'discord', 'system'
    timestamp: datetime
    user_id: Optional[str] = None
    submission_id: Optional[str] = None
    priority: int = 1  # 1=low, 5=critical

class RealTimeSyncEngine:
    def __init__(self):
        # Redis for real-time messaging
        self.redis_client = redis.Redis(
            host='localhost', 
            port=6379, 
            decode_responses=True
        )
        
        # WebSocket connections
        self.websocket_connections = set()
        self.discord_connections = set()
        
        # Event handlers
        self.event_handlers: Dict[SyncEventType, List[Callable]] = {}
        
        # Sync queues
        self.website_to_discord_queue = asyncio.Queue()
        self.discord_to_website_queue = asyncio.Queue()
        
        # Performance metrics
        self.sync_metrics = {
            'events_processed': 0,
            'sync_latency_ms': [],
            'failed_syncs': 0,
            'active_connections': 0
        }
        
        # Setup event handlers
        self.setup_event_handlers()
        
        # Start background tasks
        self.running = False
    
    def setup_event_handlers(self):
        """Setup event handlers for different sync events"""
        
        # Submission events
        self.register_handler(SyncEventType.SUBMISSION_CREATED, self.handle_submission_created)
        self.register_handler(SyncEventType.VOTE_CAST, self.handle_vote_cast)
        self.register_handler(SyncEventType.VOTE_REMOVED, self.handle_vote_removed)
        
        # Leaderboard events
        self.register_handler(SyncEventType.LEADERBOARD_UPDATED, self.handle_leaderboard_updated)
        
        # User events
        self.register_handler(SyncEventType.USER_JOINED, self.handle_user_joined)
        self.register_handler(SyncEventType.USER_PROMOTED, self.handle_user_promoted)
        
        # System events
        self.register_handler(SyncEventType.LIVE_STATS_UPDATED, self.handle_live_stats_updated)
        self.register_handler(SyncEventType.TRENDING_UPDATED, self.handle_trending_updated)
    
    def register_handler(self, event_type: SyncEventType, handler: Callable):
        """Register an event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    async def start(self):
        """Start the real-time sync engine"""
        print("🔄 Starting Real-Time Sync Engine...")
        
        self.running = True
        
        # Start background tasks
        tasks = [
            asyncio.create_task(self.process_website_to_discord()),
            asyncio.create_task(self.process_discord_to_website()),
            asyncio.create_task(self.websocket_server()),
            asyncio.create_task(self.redis_listener()),
            asyncio.create_task(self.periodic_sync_tasks()),
            asyncio.create_task(self.metrics_collector())
        ]
        
        print("✅ Real-Time Sync Engine started")
        
        # Wait for all tasks
        await asyncio.gather(*tasks)
    
    async def emit_event(self, event: SyncEvent):
        """Emit a sync event to all connected clients"""
        start_time = time.time()
        
        try:
            # Process through handlers
            if event.event_type in self.event_handlers:
                for handler in self.event_handlers[event.event_type]:
                    await handler(event)
            
            # Broadcast to WebSocket clients
            await self.broadcast_to_websockets(event)
            
            # Publish to Redis
            await self.publish_to_redis(event)
            
            # Update metrics
            latency = (time.time() - start_time) * 1000
            self.sync_metrics['sync_latency_ms'].append(latency)
            self.sync_metrics['events_processed'] += 1
            
            # Log analytics
            analytics_service.log_event('sync_event_processed', {
                'event_type': event.event_type.value,
                'source': event.source,
                'latency_ms': latency,
                'priority': event.priority
            })
            
        except Exception as e:
            self.sync_metrics['failed_syncs'] += 1
            print(f"❌ Sync event failed: {e}")
            
            analytics_service.log_event('sync_event_failed', {
                'event_type': event.event_type.value,
                'error': str(e)
            })
    
    async def handle_submission_created(self, event: SyncEvent):
        """Handle new submission creation"""
        submission_data = event.data
        
        # Post to Discord
        if discord_service.is_connected():
            discord_result = await discord_service.post_submission(
                submission_data['submission'],
                submission_data['user']
            )
            
            # Update database with Discord message ID
            if discord_result.get('success'):
                # Update submission with Discord info
                pass
        
        # Update live leaderboard
        await self.update_live_leaderboard()
        
        # Trigger trending analysis
        await self.analyze_trending_content()
    
    async def handle_vote_cast(self, event: SyncEvent):
        """Handle vote casting"""
        vote_data = event.data
        
        # Update Discord message reactions
        if discord_service.is_connected():
            # Add reaction to Discord message
            pass
        
        # Update real-time vote count
        await self.broadcast_vote_update(vote_data)
        
        # Update leaderboard
        await self.update_live_leaderboard()
        
        # Check for milestones
        await self.check_vote_milestones(vote_data)
    
    async def handle_vote_removed(self, event: SyncEvent):
        """Handle vote removal"""
        vote_data = event.data
        
        # Remove Discord reaction
        # Update vote counts
        # Refresh leaderboard
        await self.update_live_leaderboard()
    
    async def handle_leaderboard_updated(self, event: SyncEvent):
        """Handle leaderboard updates"""
        leaderboard_data = event.data
        
        # Broadcast to all clients
        await self.broadcast_to_websockets(SyncEvent(
            id=str(uuid.uuid4()),
            event_type=SyncEventType.LEADERBOARD_UPDATED,
            data=leaderboard_data,
            source='system',
            timestamp=datetime.now()
        ))
        
        # Update Discord leaderboard channel
        if discord_service.is_connected():
            await discord_service.send_leaderboard(
                discord_service.channels.get('live-leaderboard')
            )
    
    async def handle_user_joined(self, event: SyncEvent):
        """Handle new user joining"""
        user_data = event.data
        
        # Welcome message in Discord
        # Update user count
        # Trigger onboarding flow
        pass
    
    async def handle_user_promoted(self, event: SyncEvent):
        """Handle user role promotion"""
        user_data = event.data
        
        # Update Discord roles
        # Send congratulations
        # Update user stats
        pass
    
    async def handle_live_stats_updated(self, event: SyncEvent):
        """Handle live statistics updates"""
        stats_data = event.data
        
        # Broadcast to dashboard clients
        await self.broadcast_to_websockets(event)
        
        # Update Discord stats channels
        pass
    
    async def handle_trending_updated(self, event: SyncEvent):
        """Handle trending content updates"""
        trending_data = event.data
        
        # Update trending displays
        # Notify creators
        # Update social media
        pass
    
    async def broadcast_to_websockets(self, event: SyncEvent):
        """Broadcast event to all WebSocket connections"""
        if not self.websocket_connections:
            return
        
        message = json.dumps({
            'type': 'sync_event',
            'event': asdict(event),
            'timestamp': datetime.now().isoformat()
        }, default=str)
        
        # Send to all connected clients
        disconnected = set()
        for websocket in self.websocket_connections:
            try:
                await websocket.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(websocket)
        
        # Remove disconnected clients
        self.websocket_connections -= disconnected
        self.sync_metrics['active_connections'] = len(self.websocket_connections)
    
    async def publish_to_redis(self, event: SyncEvent):
        """Publish event to Redis for cross-instance sync"""
        try:
            self.redis_client.publish('hotppl_sync', json.dumps(asdict(event), default=str))
        except Exception as e:
            print(f"Redis publish failed: {e}")
    
    async def websocket_server(self):
        """WebSocket server for real-time client connections"""
        async def handle_client(websocket, path):
            self.websocket_connections.add(websocket)
            self.sync_metrics['active_connections'] = len(self.websocket_connections)
            
            try:
                # Send initial data
                await websocket.send(json.dumps({
                    'type': 'connection_established',
                    'data': {
                        'leaderboard': db.get_leaderboard(10),
                        'live_stats': await self.get_live_stats()
                    }
                }, default=str))
                
                # Keep connection alive
                async for message in websocket:
                    # Handle client messages
                    await self.handle_client_message(websocket, message)
                    
            except websockets.exceptions.ConnectionClosed:
                pass
            finally:
                self.websocket_connections.discard(websocket)
                self.sync_metrics['active_connections'] = len(self.websocket_connections)
        
        # Start WebSocket server
        start_server = websockets.serve(handle_client, "localhost", 8765)
        await start_server
    
    async def handle_client_message(self, websocket, message):
        """Handle messages from WebSocket clients"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'vote':
                # Handle vote from client
                await self.process_client_vote(data)
            elif message_type == 'request_update':
                # Send latest data
                await self.send_client_update(websocket, data.get('data_type'))
                
        except Exception as e:
            print(f"Client message error: {e}")
    
    async def redis_listener(self):
        """Listen for Redis pub/sub messages"""
        # Redis listener implementation
        pass
    
    async def periodic_sync_tasks(self):
        """Periodic synchronization tasks"""
        while self.running:
            try:
                # Update leaderboard every 30 seconds
                await self.update_live_leaderboard()
                
                # Update trending every 5 minutes
                await self.analyze_trending_content()
                
                # Update live stats every 10 seconds
                await self.update_live_stats()
                
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"Periodic sync error: {e}")
                await asyncio.sleep(30)
    
    async def update_live_leaderboard(self):
        """Update live leaderboard"""
        leaderboard = db.get_leaderboard(10)
        
        await self.emit_event(SyncEvent(
            id=str(uuid.uuid4()),
            event_type=SyncEventType.LEADERBOARD_UPDATED,
            data={'leaderboard': leaderboard},
            source='system',
            timestamp=datetime.now()
        ))
    
    async def update_live_stats(self):
        """Update live statistics"""
        stats = await self.get_live_stats()
        
        await self.emit_event(SyncEvent(
            id=str(uuid.uuid4()),
            event_type=SyncEventType.LIVE_STATS_UPDATED,
            data=stats,
            source='system',
            timestamp=datetime.now()
        ))
    
    async def get_live_stats(self) -> Dict[str, Any]:
        """Get current live statistics"""
        # Calculate live stats
        return {
            'active_users': len(self.websocket_connections),
            'total_submissions': 0,  # Get from database
            'total_votes': 0,  # Get from database
            'trending_scenes': [],  # Calculate trending
            'sync_performance': {
                'events_processed': self.sync_metrics['events_processed'],
                'average_latency': sum(self.sync_metrics['sync_latency_ms'][-100:]) / min(100, len(self.sync_metrics['sync_latency_ms'])) if self.sync_metrics['sync_latency_ms'] else 0,
                'failed_syncs': self.sync_metrics['failed_syncs']
            }
        }
    
    async def analyze_trending_content(self):
        """Analyze and update trending content"""
        # Trending analysis logic
        pass
    
    async def metrics_collector(self):
        """Collect and report performance metrics"""
        while self.running:
            try:
                # Log performance metrics
                analytics_service.log_event('sync_engine_metrics', {
                    'active_connections': len(self.websocket_connections),
                    'events_processed': self.sync_metrics['events_processed'],
                    'failed_syncs': self.sync_metrics['failed_syncs'],
                    'average_latency': sum(self.sync_metrics['sync_latency_ms'][-100:]) / min(100, len(self.sync_metrics['sync_latency_ms'])) if self.sync_metrics['sync_latency_ms'] else 0
                })
                
                await asyncio.sleep(60)  # Report every minute
                
            except Exception as e:
                print(f"Metrics collection error: {e}")
                await asyncio.sleep(60)
    
    async def stop(self):
        """Stop the sync engine"""
        self.running = False
        print("🛑 Real-Time Sync Engine stopped")

# Global sync engine instance
sync_engine = RealTimeSyncEngine()
