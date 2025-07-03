// Discord Integration for HOT PPL Platform
// This handles Discord OAuth, webhooks, and community features

class DiscordIntegration {
    constructor() {
        this.clientId = 'YOUR_DISCORD_CLIENT_ID'; // Replace with actual client ID
        this.redirectUri = 'https://hotppl.io/auth/discord';
        this.guildId = 'YOUR_GUILD_ID'; // Replace with your Discord server ID
        this.webhookUrl = 'YOUR_WEBHOOK_URL'; // Replace with webhook URL
        this.apiBase = 'https://discord.com/api/v10';
    }

    // Discord OAuth Login
    initiateDiscordLogin() {
        const scopes = ['identify', 'guilds.join', 'email'];
        const authUrl = `https://discord.com/api/oauth2/authorize?` +
            `client_id=${this.clientId}&` +
            `redirect_uri=${encodeURIComponent(this.redirectUri)}&` +
            `response_type=code&` +
            `scope=${scopes.join('%20')}`;
        
        window.location.href = authUrl;
    }

    // Handle Discord OAuth callback
    async handleDiscordCallback(code) {
        try {
            const response = await fetch('/api/discord/auth', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });
            
            const data = await response.json();
            if (data.success) {
                localStorage.setItem('discordUser', JSON.stringify(data.user));
                this.updateUIForLoggedInUser(data.user);
                return data.user;
            }
        } catch (error) {
            console.error('Discord auth error:', error);
        }
        return null;
    }

    // Send submission notification to Discord
    async notifySubmission(submissionData) {
        const embed = {
            title: "🎬 New HOT PPL Submission!",
            description: `**Scene**: ${submissionData.scene}\n**Creator**: ${submissionData.creator}`,
            color: 0xff0080, // Hot pink
            fields: [
                {
                    name: "🎭 Scene",
                    value: submissionData.scene,
                    inline: true
                },
                {
                    name: "👤 Creator",
                    value: submissionData.creator,
                    inline: true
                },
                {
                    name: "🛠️ Tools Used",
                    value: submissionData.tools || "Not specified",
                    inline: true
                }
            ],
            thumbnail: {
                url: submissionData.thumbnail || "https://hotppl.io/assets/placeholder.jpg"
            },
            footer: {
                text: "HOT PPL - Where the f*ck are all the hot people?",
                icon_url: "https://hotppl.io/assets/logo.png"
            },
            timestamp: new Date().toISOString()
        };

        try {
            await fetch(this.webhookUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    embeds: [embed],
                    content: "🚨 **NEW SUBMISSION ALERT** 🚨"
                })
            });
        } catch (error) {
            console.error('Failed to send Discord notification:', error);
        }
    }

    // Create voting thread for submission
    async createVotingThread(submissionData) {
        const threadData = {
            name: `🗳️ Vote: ${submissionData.scene} by ${submissionData.creator}`,
            type: 11, // Public thread
            auto_archive_duration: 10080 // 7 days
        };

        try {
            const response = await fetch('/api/discord/create-thread', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    channelId: 'VOTING_CHANNEL_ID',
                    threadData,
                    submissionData
                })
            });
            
            return await response.json();
        } catch (error) {
            console.error('Failed to create voting thread:', error);
        }
    }

    // Real-time voting updates via Discord
    async updateVoteCount(submissionId, newVoteCount) {
        try {
            await fetch('/api/discord/update-votes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    submissionId,
                    voteCount: newVoteCount
                })
            });
        } catch (error) {
            console.error('Failed to update Discord vote count:', error);
        }
    }

    // Get Discord user info
    getDiscordUser() {
        const userData = localStorage.getItem('discordUser');
        return userData ? JSON.parse(userData) : null;
    }

    // Update UI for logged in Discord user
    updateUIForLoggedInUser(user) {
        // Update Discord links to show user info
        const discordLinks = document.querySelectorAll('.discord-link');
        discordLinks.forEach(link => {
            link.innerHTML = `
                <img src="https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png" 
                     style="width: 24px; height: 24px; border-radius: 50%; margin-right: 8px;">
                ${user.username} - Community
            `;
        });

        // Show Discord-exclusive features
        this.showDiscordFeatures();
    }

    // Show features only available to Discord members
    showDiscordFeatures() {
        const discordFeatures = document.querySelectorAll('.discord-only');
        discordFeatures.forEach(feature => {
            feature.style.display = 'block';
        });
    }

    // Join Discord server automatically
    async joinDiscordServer(accessToken) {
        try {
            const response = await fetch('/api/discord/join-server', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ accessToken })
            });
            
            return await response.json();
        } catch (error) {
            console.error('Failed to join Discord server:', error);
        }
    }

    // Get live Discord member count
    async getDiscordStats() {
        try {
            const response = await fetch('/api/discord/stats');
            const stats = await response.json();
            
            // Update member count on website
            const memberCountElements = document.querySelectorAll('.discord-member-count');
            memberCountElements.forEach(element => {
                element.textContent = `${stats.memberCount} creators`;
            });
            
            return stats;
        } catch (error) {
            console.error('Failed to get Discord stats:', error);
        }
    }

    // Initialize Discord integration
    init() {
        // Check if user is already logged in
        const user = this.getDiscordUser();
        if (user) {
            this.updateUIForLoggedInUser(user);
        }

        // Add Discord login buttons
        this.addDiscordLoginButtons();
        
        // Get live Discord stats
        this.getDiscordStats();
        
        // Set up periodic stats updates
        setInterval(() => this.getDiscordStats(), 60000); // Update every minute
    }

    // Add Discord login buttons to the page
    addDiscordLoginButtons() {
        const discordLinks = document.querySelectorAll('.discord-link');
        discordLinks.forEach(link => {
            if (!this.getDiscordUser()) {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.initiateDiscordLogin();
                });
            }
        });
    }
}

// Initialize Discord integration when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.discordIntegration = new DiscordIntegration();
    window.discordIntegration.init();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DiscordIntegration;
}
