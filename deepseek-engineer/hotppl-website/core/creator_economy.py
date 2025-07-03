#!/usr/bin/env python3
"""
HOT PPL Creator Economy System
Advanced multi-tier reward system, collaboration matching, and monetization framework
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import json
import math
from decimal import Decimal

from database import db, User, Submission, UserRole
from analytics_service import analytics_service

class RewardTier(Enum):
    EARTHLING = "earthling"
    RISING_STAR = "rising_star"
    SCENE_MASTER = "scene_master"
    TOP_CREATOR = "top_creator"
    VIRAL_LEGEND = "viral_legend"
    ALIEN_ELITE = "alien_elite"

class RewardType(Enum):
    POINTS = "points"
    BADGES = "badges"
    EXCLUSIVE_ACCESS = "exclusive_access"
    COLLABORATION_BOOST = "collaboration_boost"
    MONETIZATION = "monetization"
    MERCHANDISE = "merchandise"
    PLATFORM_REVENUE = "platform_revenue"

class CollaborationStatus(Enum):
    OPEN = "open"
    MATCHED = "matched"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class CreatorProfile:
    user_id: str
    tier: RewardTier
    total_points: int
    reputation_score: float
    specialties: List[str]
    collaboration_rating: float
    monetization_enabled: bool
    revenue_share: float
    badges: List[str]
    achievements: List[str]
    preferred_scenes: List[str]
    availability_status: str
    portfolio_highlights: List[str]
    social_links: Dict[str, str]
    created_at: datetime
    updated_at: datetime

@dataclass
class RewardTransaction:
    id: str
    user_id: str
    reward_type: RewardType
    amount: float
    reason: str
    submission_id: Optional[str]
    collaboration_id: Optional[str]
    metadata: Dict[str, Any]
    created_at: datetime

@dataclass
class CollaborationRequest:
    id: str
    requester_id: str
    target_id: Optional[str]
    scene_name: str
    description: str
    required_skills: List[str]
    reward_split: Dict[str, float]
    deadline: Optional[datetime]
    status: CollaborationStatus
    applications: List[str]
    selected_collaborator: Optional[str]
    created_at: datetime
    updated_at: datetime

class AdvancedCreatorEconomy:
    def __init__(self):
        # Reward configuration
        self.tier_requirements = {
            RewardTier.EARTHLING: {'points': 0, 'submissions': 0},
            RewardTier.RISING_STAR: {'points': 100, 'submissions': 3},
            RewardTier.SCENE_MASTER: {'points': 500, 'submissions': 10},
            RewardTier.TOP_CREATOR: {'points': 2000, 'submissions': 25},
            RewardTier.VIRAL_LEGEND: {'points': 10000, 'submissions': 50},
            RewardTier.ALIEN_ELITE: {'points': 50000, 'submissions': 100}
        }
        
        # Point values for different actions
        self.point_values = {
            'submission_created': 10,
            'vote_received': 2,
            'featured_submission': 100,
            'viral_submission': 500,
            'collaboration_completed': 50,
            'community_help': 5,
            'daily_login': 1,
            'scene_mastery': 200,
            'trend_setter': 300
        }
        
        # Revenue sharing configuration
        self.revenue_shares = {
            RewardTier.EARTHLING: 0.0,
            RewardTier.RISING_STAR: 0.1,
            RewardTier.SCENE_MASTER: 0.2,
            RewardTier.TOP_CREATOR: 0.35,
            RewardTier.VIRAL_LEGEND: 0.5,
            RewardTier.ALIEN_ELITE: 0.7
        }
        
        # Collaboration matching algorithm
        self.collaboration_matcher = CollaborationMatcher()
        
        # Monetization system
        self.monetization_system = MonetizationSystem()
        
        # Performance tracking
        self.economy_metrics = {
            'total_points_distributed': 0,
            'active_collaborations': 0,
            'revenue_generated': Decimal('0.00'),
            'creator_retention_rate': 0.0
        }
    
    async def initialize_creator_profile(self, user: User) -> CreatorProfile:
        """Initialize creator profile for new user"""
        profile = CreatorProfile(
            user_id=user.id,
            tier=RewardTier.EARTHLING,
            total_points=0,
            reputation_score=5.0,  # Start with neutral reputation
            specialties=[],
            collaboration_rating=5.0,
            monetization_enabled=False,
            revenue_share=0.0,
            badges=[],
            achievements=[],
            preferred_scenes=[],
            availability_status='available',
            portfolio_highlights=[],
            social_links={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Store profile
        await self.store_creator_profile(profile)
        
        # Award welcome bonus
        await self.award_points(user.id, 25, "Welcome to HOT PPL!")
        
        return profile
    
    async def award_points(self, user_id: str, points: int, reason: str, 
                          submission_id: str = None, collaboration_id: str = None) -> RewardTransaction:
        """Award points to a creator"""
        transaction = RewardTransaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            reward_type=RewardType.POINTS,
            amount=float(points),
            reason=reason,
            submission_id=submission_id,
            collaboration_id=collaboration_id,
            metadata={'timestamp': datetime.now().isoformat()},
            created_at=datetime.now()
        )
        
        # Update creator profile
        profile = await self.get_creator_profile(user_id)
        if profile:
            profile.total_points += points
            
            # Check for tier promotion
            new_tier = self.calculate_tier(profile.total_points, await self.get_user_submission_count(user_id))
            if new_tier != profile.tier:
                await self.promote_creator(profile, new_tier)
            
            profile.updated_at = datetime.now()
            await self.store_creator_profile(profile)
        
        # Store transaction
        await self.store_reward_transaction(transaction)
        
        # Update metrics
        self.economy_metrics['total_points_distributed'] += points
        
        # Log analytics
        analytics_service.log_event('points_awarded', {
            'user_id': user_id,
            'points': points,
            'reason': reason,
            'total_points': profile.total_points if profile else points
        })
        
        return transaction
    
    async def promote_creator(self, profile: CreatorProfile, new_tier: RewardTier):
        """Promote creator to new tier"""
        old_tier = profile.tier
        profile.tier = new_tier
        profile.revenue_share = self.revenue_shares[new_tier]
        
        # Award tier-specific benefits
        await self.award_tier_benefits(profile, new_tier)
        
        # Enable monetization for higher tiers
        if new_tier.value in ['top_creator', 'viral_legend', 'alien_elite']:
            profile.monetization_enabled = True
        
        # Log promotion
        analytics_service.log_event('creator_promoted', {
            'user_id': profile.user_id,
            'old_tier': old_tier.value,
            'new_tier': new_tier.value,
            'total_points': profile.total_points
        })
        
        print(f"🎉 Creator {profile.user_id} promoted to {new_tier.value}")
    
    async def award_tier_benefits(self, profile: CreatorProfile, tier: RewardTier):
        """Award tier-specific benefits"""
        benefits = {
            RewardTier.RISING_STAR: {
                'badges': ['Rising Star'],
                'exclusive_access': ['early_challenges'],
                'bonus_points': 50
            },
            RewardTier.SCENE_MASTER: {
                'badges': ['Scene Master'],
                'exclusive_access': ['creator_lounge', 'advanced_tools'],
                'bonus_points': 200
            },
            RewardTier.TOP_CREATOR: {
                'badges': ['Top Creator'],
                'exclusive_access': ['vip_discord', 'monetization'],
                'bonus_points': 500
            },
            RewardTier.VIRAL_LEGEND: {
                'badges': ['Viral Legend'],
                'exclusive_access': ['legend_tier', 'revenue_sharing'],
                'bonus_points': 1000
            },
            RewardTier.ALIEN_ELITE: {
                'badges': ['Alien Elite'],
                'exclusive_access': ['elite_tier', 'platform_governance'],
                'bonus_points': 2000
            }
        }
        
        tier_benefits = benefits.get(tier, {})
        
        # Award badges
        for badge in tier_benefits.get('badges', []):
            if badge not in profile.badges:
                profile.badges.append(badge)
        
        # Award bonus points
        bonus_points = tier_benefits.get('bonus_points', 0)
        if bonus_points > 0:
            await self.award_points(profile.user_id, bonus_points, f"Tier promotion bonus: {tier.value}")
    
    def calculate_tier(self, total_points: int, submission_count: int) -> RewardTier:
        """Calculate creator tier based on points and submissions"""
        for tier in reversed(list(RewardTier)):
            requirements = self.tier_requirements[tier]
            if (total_points >= requirements['points'] and 
                submission_count >= requirements['submissions']):
                return tier
        return RewardTier.EARTHLING
    
    async def process_submission_rewards(self, submission: Submission, analysis_results: Dict):
        """Process rewards for a new submission"""
        user_id = submission.user_id
        
        # Base submission reward
        base_points = self.point_values['submission_created']
        await self.award_points(user_id, base_points, "New submission", submission.id)
        
        # Quality bonus
        quality_score = analysis_results.get('quality_score', 0.0)
        if quality_score > 0.8:
            quality_bonus = int(quality_score * 50)
            await self.award_points(user_id, quality_bonus, "High quality submission", submission.id)
        
        # Creativity bonus
        creativity_score = analysis_results.get('creativity_score', 0.0)
        if creativity_score > 0.7:
            creativity_bonus = int(creativity_score * 30)
            await self.award_points(user_id, creativity_bonus, "Creative submission", submission.id)
        
        # Viral potential bonus
        viral_potential = analysis_results.get('viral_potential', 0.0)
        if viral_potential > 0.8:
            viral_bonus = self.point_values['viral_submission']
            await self.award_points(user_id, viral_bonus, "Viral potential submission", submission.id)
        
        # Scene mastery tracking
        await self.track_scene_mastery(user_id, submission.scene_name)
    
    async def track_scene_mastery(self, user_id: str, scene_name: str):
        """Track and reward scene mastery"""
        # Count submissions for this scene
        scene_submissions = await self.get_user_scene_submissions(user_id, scene_name)
        
        # Award mastery at milestones
        mastery_milestones = {5: 100, 10: 300, 20: 500}
        
        if len(scene_submissions) in mastery_milestones:
            mastery_points = mastery_milestones[len(scene_submissions)]
            await self.award_points(user_id, mastery_points, f"Scene mastery: {scene_name}")
            
            # Add to specialties
            profile = await self.get_creator_profile(user_id)
            if profile and scene_name not in profile.specialties:
                profile.specialties.append(scene_name)
                await self.store_creator_profile(profile)
    
    async def process_vote_rewards(self, vote_data: Dict):
        """Process rewards for receiving votes"""
        submission_id = vote_data['submission_id']
        submission = await self.get_submission(submission_id)
        
        if submission:
            vote_points = self.point_values['vote_received']
            await self.award_points(submission.user_id, vote_points, "Vote received", submission_id)
            
            # Milestone bonuses
            vote_count = vote_data.get('new_vote_count', 0)
            milestones = {10: 20, 50: 100, 100: 300, 500: 1000}
            
            if vote_count in milestones:
                milestone_bonus = milestones[vote_count]
                await self.award_points(submission.user_id, milestone_bonus, 
                                      f"Vote milestone: {vote_count} votes", submission_id)
    
    async def create_collaboration_request(self, requester_id: str, scene_name: str, 
                                         description: str, required_skills: List[str],
                                         reward_split: Dict[str, float] = None) -> CollaborationRequest:
        """Create a new collaboration request"""
        if reward_split is None:
            reward_split = {'requester': 0.6, 'collaborator': 0.4}
        
        collaboration = CollaborationRequest(
            id=str(uuid.uuid4()),
            requester_id=requester_id,
            target_id=None,
            scene_name=scene_name,
            description=description,
            required_skills=required_skills,
            reward_split=reward_split,
            deadline=None,
            status=CollaborationStatus.OPEN,
            applications=[],
            selected_collaborator=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Store collaboration
        await self.store_collaboration_request(collaboration)
        
        # Find potential matches
        matches = await self.collaboration_matcher.find_matches(collaboration)
        
        # Notify potential collaborators
        await self.notify_potential_collaborators(collaboration, matches)
        
        return collaboration
    
    async def apply_for_collaboration(self, collaboration_id: str, applicant_id: str) -> bool:
        """Apply for a collaboration"""
        collaboration = await self.get_collaboration_request(collaboration_id)
        
        if not collaboration or collaboration.status != CollaborationStatus.OPEN:
            return False
        
        if applicant_id not in collaboration.applications:
            collaboration.applications.append(applicant_id)
            collaboration.updated_at = datetime.now()
            await self.store_collaboration_request(collaboration)
            
            # Notify requester
            await self.notify_collaboration_application(collaboration, applicant_id)
            
            return True
        
        return False
    
    async def select_collaborator(self, collaboration_id: str, selected_id: str) -> bool:
        """Select a collaborator for a request"""
        collaboration = await self.get_collaboration_request(collaboration_id)
        
        if not collaboration or selected_id not in collaboration.applications:
            return False
        
        collaboration.selected_collaborator = selected_id
        collaboration.status = CollaborationStatus.MATCHED
        collaboration.updated_at = datetime.now()
        
        await self.store_collaboration_request(collaboration)
        
        # Notify selected collaborator
        await self.notify_collaboration_selection(collaboration)
        
        # Update metrics
        self.economy_metrics['active_collaborations'] += 1
        
        return True
    
    async def complete_collaboration(self, collaboration_id: str, submission_id: str):
        """Complete a collaboration and distribute rewards"""
        collaboration = await self.get_collaboration_request(collaboration_id)
        
        if not collaboration or collaboration.status != CollaborationStatus.IN_PROGRESS:
            return
        
        collaboration.status = CollaborationStatus.COMPLETED
        collaboration.updated_at = datetime.now()
        
        # Calculate and distribute rewards
        base_reward = self.point_values['collaboration_completed']
        
        requester_reward = int(base_reward * collaboration.reward_split['requester'])
        collaborator_reward = int(base_reward * collaboration.reward_split['collaborator'])
        
        await self.award_points(collaboration.requester_id, requester_reward, 
                              "Collaboration completed", submission_id, collaboration_id)
        await self.award_points(collaboration.selected_collaborator, collaborator_reward,
                              "Collaboration completed", submission_id, collaboration_id)
        
        # Update collaboration ratings
        await self.update_collaboration_ratings(collaboration)
        
        await self.store_collaboration_request(collaboration)
        
        self.economy_metrics['active_collaborations'] -= 1
    
    # Storage and retrieval methods
    async def store_creator_profile(self, profile: CreatorProfile):
        """Store creator profile in database"""
        # Implementation would store in database
        pass
    
    async def get_creator_profile(self, user_id: str) -> Optional[CreatorProfile]:
        """Get creator profile from database"""
        # Implementation would retrieve from database
        return None
    
    async def store_reward_transaction(self, transaction: RewardTransaction):
        """Store reward transaction in database"""
        # Implementation would store in database
        pass
    
    async def store_collaboration_request(self, collaboration: CollaborationRequest):
        """Store collaboration request in database"""
        # Implementation would store in database
        pass
    
    async def get_collaboration_request(self, collaboration_id: str) -> Optional[CollaborationRequest]:
        """Get collaboration request from database"""
        # Implementation would retrieve from database
        return None
    
    # Additional helper methods...
    async def get_user_submission_count(self, user_id: str) -> int:
        """Get user's total submission count"""
        return 0  # Placeholder
    
    async def get_user_scene_submissions(self, user_id: str, scene_name: str) -> List:
        """Get user's submissions for a specific scene"""
        return []  # Placeholder
    
    async def get_submission(self, submission_id: str) -> Optional[Submission]:
        """Get submission by ID"""
        return None  # Placeholder

class CollaborationMatcher:
    """Advanced collaboration matching algorithm"""
    
    async def find_matches(self, collaboration: CollaborationRequest) -> List[str]:
        """Find potential collaboration matches"""
        # Implementation would use ML algorithms to match creators
        return []

class MonetizationSystem:
    """Creator monetization and revenue sharing system"""
    
    async def process_revenue_share(self, creator_id: str, revenue: Decimal):
        """Process revenue sharing for creators"""
        # Implementation would handle payments and revenue distribution
        pass

# Global creator economy instance
creator_economy = AdvancedCreatorEconomy()
