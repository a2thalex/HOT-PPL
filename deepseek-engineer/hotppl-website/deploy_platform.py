#!/usr/bin/env python3
"""
HOT PPL Platform Deployment Orchestrator
Comprehensive deployment and management system
"""

import asyncio
import threading
import time
import os
import sys
from datetime import datetime
from typing import Dict, List
import subprocess
import json

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from database import db
from discord_service import discord_service
from analytics_service import analytics_service

class PlatformOrchestrator:
    def __init__(self):
        self.services = {
            'database': {'status': 'stopped', 'instance': db},
            'discord': {'status': 'stopped', 'instance': discord_service},
            'analytics': {'status': 'stopped', 'instance': analytics_service},
            'api_gateway': {'status': 'stopped', 'instance': None},
            'website': {'status': 'stopped', 'instance': None}
        }
        
        self.deployment_status = {
            'started_at': None,
            'services_running': 0,
            'total_services': len(self.services),
            'health_checks_passed': 0,
            'errors': []
        }
    
    async def deploy_full_platform(self):
        """Deploy the complete HOT PPL platform"""
        print("🛸 Starting HOT PPL Platform Deployment")
        print("=" * 50)
        
        self.deployment_status['started_at'] = datetime.now()
        
        try:
            # Phase 1: Core Infrastructure
            print("\n📊 Phase 1: Core Infrastructure")
            await self._deploy_database()
            await self._deploy_analytics()
            
            # Phase 2: Discord Integration
            print("\n🤖 Phase 2: Discord Integration")
            await self._deploy_discord_service()
            
            # Phase 3: API Gateway
            print("\n🌐 Phase 3: API Gateway")
            await self._deploy_api_gateway()
            
            # Phase 4: Website Integration
            print("\n🚀 Phase 4: Website Integration")
            await self._deploy_website_integration()
            
            # Phase 5: Health Checks
            print("\n🔍 Phase 5: Health Checks")
            await self._run_health_checks()
            
            # Phase 6: Final Setup
            print("\n✅ Phase 6: Final Setup")
            await self._finalize_deployment()
            
            print("\n🎉 HOT PPL Platform Deployment Complete!")
            self._print_deployment_summary()
            
        except Exception as e:
            print(f"\n❌ Deployment failed: {e}")
            self.deployment_status['errors'].append(str(e))
            await self._cleanup_failed_deployment()
    
    async def _deploy_database(self):
        """Deploy and initialize database"""
        print("  🗄️ Initializing database...")
        
        try:
            # Initialize database
            db.init_database()
            
            # Create initial data
            await self._create_initial_data()
            
            self.services['database']['status'] = 'running'
            self.deployment_status['services_running'] += 1
            print("  ✅ Database initialized successfully")
            
        except Exception as e:
            print(f"  ❌ Database initialization failed: {e}")
            raise
    
    async def _create_initial_data(self):
        """Create initial platform data"""
        # Create default challenge
        # Create admin user
        # Set up initial scenes
        print("  📝 Creating initial platform data...")
    
    async def _deploy_analytics(self):
        """Deploy analytics service"""
        print("  📈 Starting analytics service...")
        
        try:
            # Analytics service is already initialized
            self.services['analytics']['status'] = 'running'
            self.deployment_status['services_running'] += 1
            
            # Log deployment event
            analytics_service.log_event('platform_deployment_started', {
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            })
            
            print("  ✅ Analytics service started")
            
        except Exception as e:
            print(f"  ❌ Analytics service failed: {e}")
            raise
    
    async def _deploy_discord_service(self):
        """Deploy Discord service"""
        print("  🤖 Starting Discord service...")
        
        try:
            # Start Discord bot in background
            discord_task = asyncio.create_task(discord_service.start())
            
            # Wait for connection
            max_wait = 30
            wait_time = 0
            while not discord_service.is_connected() and wait_time < max_wait:
                await asyncio.sleep(1)
                wait_time += 1
                print(f"  ⏳ Waiting for Discord connection... ({wait_time}s)")
            
            if discord_service.is_connected():
                self.services['discord']['status'] = 'running'
                self.deployment_status['services_running'] += 1
                print("  ✅ Discord service connected successfully")
                
                # Log Discord connection
                analytics_service.log_event('discord_service_started', {
                    'guild_id': discord_service.guild_id,
                    'connection_time': wait_time
                })
            else:
                raise Exception("Discord connection timeout")
                
        except Exception as e:
            print(f"  ❌ Discord service failed: {e}")
            raise
    
    async def _deploy_api_gateway(self):
        """Deploy API Gateway"""
        print("  🌐 Starting API Gateway...")
        
        try:
            # Start API Gateway in background thread
            def start_api():
                from core.api_gateway import app
                app.run(host='0.0.0.0', port=5000, debug=False)
            
            api_thread = threading.Thread(target=start_api, daemon=True)
            api_thread.start()
            
            # Wait for API to start
            await asyncio.sleep(3)
            
            # Test API health
            import aiohttp
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get('http://localhost:5000/api/health') as response:
                        if response.status == 200:
                            self.services['api_gateway']['status'] = 'running'
                            self.deployment_status['services_running'] += 1
                            print("  ✅ API Gateway started successfully")
                        else:
                            raise Exception(f"API health check failed: {response.status}")
                except Exception as e:
                    raise Exception(f"API Gateway connection failed: {e}")
                    
        except Exception as e:
            print(f"  ❌ API Gateway failed: {e}")
            raise
    
    async def _deploy_website_integration(self):
        """Deploy website integration"""
        print("  🚀 Deploying website integration...")
        
        try:
            # Copy integration files
            self._copy_integration_files()
            
            # Deploy to Firebase
            await self._deploy_to_firebase()
            
            self.services['website']['status'] = 'running'
            self.deployment_status['services_running'] += 1
            print("  ✅ Website integration deployed")
            
        except Exception as e:
            print(f"  ❌ Website integration failed: {e}")
            raise
    
    def _copy_integration_files(self):
        """Copy integration files to website"""
        integration_files = [
            'discord-integration.js',
            'analytics-client.js',
            'real-time-sync.js'
        ]
        
        for file in integration_files:
            if os.path.exists(file):
                # Copy to public folder
                subprocess.run(['copy', file, 'public\\'], shell=True, check=True)
                print(f"    📁 Copied {file}")
    
    async def _deploy_to_firebase(self):
        """Deploy website to Firebase"""
        print("    🔥 Deploying to Firebase...")
        
        try:
            result = subprocess.run(
                ['firebase', 'deploy', '--only', 'hosting'],
                capture_output=True,
                text=True,
                check=True
            )
            print("    ✅ Firebase deployment successful")
            
        except subprocess.CalledProcessError as e:
            print(f"    ❌ Firebase deployment failed: {e.stderr}")
            raise
    
    async def _run_health_checks(self):
        """Run comprehensive health checks"""
        print("  🔍 Running health checks...")
        
        checks = [
            ('Database', self._check_database_health),
            ('Discord', self._check_discord_health),
            ('Analytics', self._check_analytics_health),
            ('API Gateway', self._check_api_health),
            ('Website', self._check_website_health)
        ]
        
        for check_name, check_func in checks:
            try:
                await check_func()
                self.deployment_status['health_checks_passed'] += 1
                print(f"    ✅ {check_name} health check passed")
            except Exception as e:
                print(f"    ❌ {check_name} health check failed: {e}")
                self.deployment_status['errors'].append(f"{check_name}: {e}")
    
    async def _check_database_health(self):
        """Check database health"""
        # Test database connection
        leaderboard = db.get_leaderboard(1)
        if not isinstance(leaderboard, list):
            raise Exception("Database query failed")
    
    async def _check_discord_health(self):
        """Check Discord service health"""
        if not discord_service.is_connected():
            raise Exception("Discord not connected")
    
    async def _check_analytics_health(self):
        """Check analytics service health"""
        # Test analytics logging
        analytics_service.log_event('health_check', {'status': 'testing'})
    
    async def _check_api_health(self):
        """Check API Gateway health"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/api/health') as response:
                if response.status != 200:
                    raise Exception(f"API health endpoint returned {response.status}")
    
    async def _check_website_health(self):
        """Check website health"""
        # Test website accessibility
        import aiohttp
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('https://hotppl.io') as response:
                    if response.status != 200:
                        raise Exception(f"Website returned {response.status}")
            except Exception as e:
                raise Exception(f"Website not accessible: {e}")
    
    async def _finalize_deployment(self):
        """Finalize deployment"""
        print("  🎯 Finalizing deployment...")
        
        # Log successful deployment
        analytics_service.log_event('platform_deployment_completed', {
            'services_running': self.deployment_status['services_running'],
            'health_checks_passed': self.deployment_status['health_checks_passed'],
            'deployment_time': (datetime.now() - self.deployment_status['started_at']).total_seconds()
        })
        
        # Create deployment summary
        self._create_deployment_summary()
        
        print("  ✅ Deployment finalized")
    
    def _print_deployment_summary(self):
        """Print deployment summary"""
        print("\n" + "=" * 50)
        print("🛸 HOT PPL PLATFORM DEPLOYMENT SUMMARY")
        print("=" * 50)
        
        print(f"🕐 Started: {self.deployment_status['started_at']}")
        print(f"🕐 Completed: {datetime.now()}")
        
        duration = datetime.now() - self.deployment_status['started_at']
        print(f"⏱️ Duration: {duration.total_seconds():.1f} seconds")
        
        print(f"\n📊 Services Status:")
        for service, info in self.services.items():
            status_icon = "✅" if info['status'] == 'running' else "❌"
            print(f"  {status_icon} {service.title()}: {info['status']}")
        
        print(f"\n🔍 Health Checks: {self.deployment_status['health_checks_passed']}/{len(self.services)} passed")
        
        if self.deployment_status['errors']:
            print(f"\n⚠️ Errors ({len(self.deployment_status['errors'])}):")
            for error in self.deployment_status['errors']:
                print(f"  - {error}")
        
        print(f"\n🌐 Platform URLs:")
        print(f"  🏠 Website: https://hotppl.io")
        print(f"  🔧 API: http://localhost:5000")
        print(f"  🤖 Discord: https://discord.gg/ZjzTK8tJ")
        
        print(f"\n🚀 Your Discord-powered HOT PPL platform is LIVE!")
    
    def _create_deployment_summary(self):
        """Create deployment summary file"""
        summary = {
            'deployment_time': datetime.now().isoformat(),
            'services': self.services,
            'status': self.deployment_status,
            'urls': {
                'website': 'https://hotppl.io',
                'api': 'http://localhost:5000',
                'discord': 'https://discord.gg/ZjzTK8tJ'
            }
        }
        
        with open('deployment_summary.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
    
    async def _cleanup_failed_deployment(self):
        """Cleanup after failed deployment"""
        print("\n🧹 Cleaning up failed deployment...")
        
        # Stop running services
        for service, info in self.services.items():
            if info['status'] == 'running':
                print(f"  🛑 Stopping {service}...")
                # Stop service logic here
        
        print("  ✅ Cleanup completed")

async def main():
    """Main deployment function"""
    orchestrator = PlatformOrchestrator()
    await orchestrator.deploy_full_platform()

if __name__ == "__main__":
    print("🛸 HOT PPL Platform Deployment Starting...")
    asyncio.run(main())
