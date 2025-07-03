/**
 * HOT PPL Real-Time Client
 * Advanced real-time synchronization for the website
 */

class HotPPLRealTimeClient {
    constructor() {
        this.websocket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectDelay = 1000;
        this.isConnected = false;
        
        // Event handlers
        this.eventHandlers = new Map();
        
        // Live data cache
        this.liveData = {
            leaderboard: [],
            liveStats: {},
            trending: [],
            userStats: {}
        };
        
        // Performance metrics
        this.metrics = {
            messagesReceived: 0,
            lastLatency: 0,
            connectionUptime: 0,
            reconnections: 0
        };
        
        this.init();
    }
    
    init() {
        this.connect();
        this.setupEventHandlers();
        this.startHeartbeat();
        
        // Auto-reconnect on page visibility change
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && !this.isConnected) {
                this.connect();
            }
        });
    }
    
    connect() {
        try {
            // Use secure WebSocket in production
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const host = window.location.hostname === 'localhost' ? 'localhost:8765' : 'api.hotppl.io:8765';
            
            this.websocket = new WebSocket(`${protocol}//${host}`);
            
            this.websocket.onopen = (event) => {
                console.log('🔄 Real-time connection established');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.metrics.connectionUptime = Date.now();
                
                // Show connection status
                this.updateConnectionStatus('connected');
                
                // Request initial data
                this.send({
                    type: 'request_update',
                    data_type: 'all'
                });
            };
            
            this.websocket.onmessage = (event) => {
                this.handleMessage(JSON.parse(event.data));
            };
            
            this.websocket.onclose = (event) => {
                console.log('🔌 Real-time connection closed');
                this.isConnected = false;
                this.updateConnectionStatus('disconnected');
                
                // Auto-reconnect
                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    setTimeout(() => {
                        this.reconnectAttempts++;
                        this.metrics.reconnections++;
                        console.log(`🔄 Reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
                        this.connect();
                    }, this.reconnectDelay * this.reconnectAttempts);
                }
            };
            
            this.websocket.onerror = (error) => {
                console.error('❌ WebSocket error:', error);
                this.updateConnectionStatus('error');
            };
            
        } catch (error) {
            console.error('❌ Connection failed:', error);
            this.updateConnectionStatus('error');
        }
    }
    
    handleMessage(message) {
        this.metrics.messagesReceived++;
        
        const { type, event, data, timestamp } = message;
        
        // Calculate latency
        if (timestamp) {
            this.metrics.lastLatency = Date.now() - new Date(timestamp).getTime();
        }
        
        switch (type) {
            case 'connection_established':
                this.handleConnectionEstablished(data);
                break;
                
            case 'sync_event':
                this.handleSyncEvent(event);
                break;
                
            case 'live_update':
                this.handleLiveUpdate(data);
                break;
                
            default:
                console.log('Unknown message type:', type);
        }
    }
    
    handleConnectionEstablished(data) {
        console.log('✅ Initial data received');
        
        // Update live data
        if (data.leaderboard) {
            this.liveData.leaderboard = data.leaderboard;
            this.updateLeaderboardDisplay();
        }
        
        if (data.live_stats) {
            this.liveData.liveStats = data.live_stats;
            this.updateLiveStatsDisplay();
        }
        
        // Trigger custom event
        this.emit('connected', data);
    }
    
    handleSyncEvent(event) {
        const { event_type, data } = event;
        
        switch (event_type) {
            case 'submission_created':
                this.handleNewSubmission(data);
                break;
                
            case 'vote_cast':
                this.handleVoteCast(data);
                break;
                
            case 'leaderboard_updated':
                this.handleLeaderboardUpdate(data);
                break;
                
            case 'live_stats_updated':
                this.handleLiveStatsUpdate(data);
                break;
                
            case 'trending_updated':
                this.handleTrendingUpdate(data);
                break;
                
            default:
                console.log('Unknown sync event:', event_type);
        }
        
        // Trigger custom event
        this.emit('sync_event', event);
    }
    
    handleNewSubmission(data) {
        console.log('🎬 New submission:', data);
        
        // Show notification
        this.showNotification('🎬 New submission!', `${data.creator} just submitted "${data.scene}"`);
        
        // Update submission count
        this.updateSubmissionCount();
        
        // Trigger custom event
        this.emit('new_submission', data);
    }
    
    handleVoteCast(data) {
        console.log('🔥 Vote cast:', data);
        
        // Update vote display
        this.updateVoteDisplay(data.submission_id, data.new_vote_count);
        
        // Show vote animation
        this.showVoteAnimation(data);
        
        // Trigger custom event
        this.emit('vote_cast', data);
    }
    
    handleLeaderboardUpdate(data) {
        console.log('🏆 Leaderboard updated');
        
        this.liveData.leaderboard = data.leaderboard;
        this.updateLeaderboardDisplay();
        
        // Trigger custom event
        this.emit('leaderboard_updated', data);
    }
    
    handleLiveStatsUpdate(data) {
        this.liveData.liveStats = data;
        this.updateLiveStatsDisplay();
        
        // Trigger custom event
        this.emit('live_stats_updated', data);
    }
    
    handleTrendingUpdate(data) {
        this.liveData.trending = data.trending_submissions;
        this.updateTrendingDisplay();
        
        // Trigger custom event
        this.emit('trending_updated', data);
    }
    
    // UI Update Methods
    updateLeaderboardDisplay() {
        const leaderboardElement = document.querySelector('.live-leaderboard');
        if (!leaderboardElement) return;
        
        const html = this.liveData.leaderboard.map((entry, index) => {
            const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `${index + 1}.`;
            return `
                <div class="leaderboard-entry" data-rank="${index + 1}">
                    <span class="rank">${medal}</span>
                    <span class="creator">${entry.username}</span>
                    <span class="scene">${entry.scene_name}</span>
                    <span class="votes">${entry.vote_count} 🔥</span>
                </div>
            `;
        }).join('');
        
        leaderboardElement.innerHTML = html;
        
        // Add animation
        leaderboardElement.classList.add('updated');
        setTimeout(() => leaderboardElement.classList.remove('updated'), 1000);
    }
    
    updateLiveStatsDisplay() {
        const stats = this.liveData.liveStats;
        
        // Update various stat displays
        this.updateElement('.stat-active-users', stats.active_users);
        this.updateElement('.stat-total-submissions', stats.total_submissions);
        this.updateElement('.stat-total-votes', stats.total_votes);
        
        // Update connection quality indicator
        if (stats.sync_performance) {
            this.updateConnectionQuality(stats.sync_performance.average_latency);
        }
    }
    
    updateVoteDisplay(submissionId, newVoteCount) {
        const voteElement = document.querySelector(`[data-submission-id="${submissionId}"] .vote-count`);
        if (voteElement) {
            voteElement.textContent = `${newVoteCount} 🔥`;
            voteElement.classList.add('vote-updated');
            setTimeout(() => voteElement.classList.remove('vote-updated'), 500);
        }
    }
    
    updateSubmissionCount() {
        const countElement = document.querySelector('.submission-count');
        if (countElement) {
            const current = parseInt(countElement.textContent) || 0;
            countElement.textContent = current + 1;
            countElement.classList.add('count-updated');
            setTimeout(() => countElement.classList.remove('count-updated'), 500);
        }
    }
    
    updateTrendingDisplay() {
        const trendingElement = document.querySelector('.trending-submissions');
        if (!trendingElement) return;
        
        const html = this.liveData.trending.map(entry => `
            <div class="trending-entry">
                <span class="title">${entry.title}</span>
                <span class="creator">by ${entry.creator}</span>
                <span class="votes">${entry.votes} 🔥</span>
            </div>
        `).join('');
        
        trendingElement.innerHTML = html;
    }
    
    updateConnectionStatus(status) {
        const statusElement = document.querySelector('.connection-status');
        if (statusElement) {
            statusElement.className = `connection-status ${status}`;
            statusElement.textContent = status === 'connected' ? '🟢 Live' : 
                                     status === 'disconnected' ? '🔴 Offline' : 
                                     '🟡 Connecting...';
        }
    }
    
    updateConnectionQuality(latency) {
        const qualityElement = document.querySelector('.connection-quality');
        if (qualityElement) {
            const quality = latency < 100 ? 'excellent' : 
                           latency < 300 ? 'good' : 
                           latency < 500 ? 'fair' : 'poor';
            
            qualityElement.className = `connection-quality ${quality}`;
            qualityElement.textContent = `${latency}ms`;
        }
    }
    
    updateElement(selector, value) {
        const element = document.querySelector(selector);
        if (element) {
            element.textContent = value;
        }
    }
    
    // Utility Methods
    showNotification(title, message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'live-notification';
        notification.innerHTML = `
            <div class="notification-title">${title}</div>
            <div class="notification-message">${message}</div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
    
    showVoteAnimation(data) {
        // Create vote animation
        const animation = document.createElement('div');
        animation.className = 'vote-animation';
        animation.textContent = '🔥 +1';
        
        // Position near the voted submission
        const submissionElement = document.querySelector(`[data-submission-id="${data.submission_id}"]`);
        if (submissionElement) {
            const rect = submissionElement.getBoundingClientRect();
            animation.style.position = 'fixed';
            animation.style.left = `${rect.right - 50}px`;
            animation.style.top = `${rect.top}px`;
            animation.style.zIndex = '9999';
        }
        
        document.body.appendChild(animation);
        
        // Animate and remove
        setTimeout(() => animation.remove(), 2000);
    }
    
    startHeartbeat() {
        setInterval(() => {
            if (this.isConnected) {
                this.send({ type: 'heartbeat', timestamp: Date.now() });
            }
        }, 30000); // Every 30 seconds
    }
    
    // Public API
    send(data) {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify(data));
        }
    }
    
    vote(submissionId, voteType = 'fire') {
        this.send({
            type: 'vote',
            submission_id: submissionId,
            vote_type: voteType,
            timestamp: Date.now()
        });
    }
    
    on(event, handler) {
        if (!this.eventHandlers.has(event)) {
            this.eventHandlers.set(event, []);
        }
        this.eventHandlers.get(event).push(handler);
    }
    
    emit(event, data) {
        if (this.eventHandlers.has(event)) {
            this.eventHandlers.get(event).forEach(handler => handler(data));
        }
    }
    
    getMetrics() {
        return {
            ...this.metrics,
            connectionUptime: this.isConnected ? Date.now() - this.metrics.connectionUptime : 0,
            isConnected: this.isConnected
        };
    }
    
    disconnect() {
        if (this.websocket) {
            this.websocket.close();
        }
    }
}

// Initialize real-time client
const hotpplRealTime = new HotPPLRealTimeClient();

// Global API
window.hotpplRealTime = hotpplRealTime;

// Auto-setup for common elements
document.addEventListener('DOMContentLoaded', () => {
    // Setup vote buttons
    document.querySelectorAll('.vote-button').forEach(button => {
        button.addEventListener('click', (e) => {
            const submissionId = e.target.dataset.submissionId;
            const voteType = e.target.dataset.voteType || 'fire';
            hotpplRealTime.vote(submissionId, voteType);
        });
    });
    
    // Setup real-time displays
    if (document.querySelector('.live-leaderboard')) {
        hotpplRealTime.on('leaderboard_updated', () => {
            console.log('🏆 Leaderboard display updated');
        });
    }
    
    if (document.querySelector('.live-stats')) {
        hotpplRealTime.on('live_stats_updated', () => {
            console.log('📊 Live stats updated');
        });
    }
});

console.log('🔄 HOT PPL Real-Time Client initialized');
