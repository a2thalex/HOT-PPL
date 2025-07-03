#!/usr/bin/env node

// HOT PPL DNS Setup Script for Namecheap
// This script configures DNS records for hotppl.io to point to Google App Engine

const fs = require('fs');
const { execSync } = require('child_process');

console.log('🌐 Setting up DNS for hotppl.io...');

// Check if config file exists
if (!fs.existsSync('./namecheap-config.json')) {
    console.error('❌ namecheap-config.json not found!');
    console.log('Please create namecheap-config.json with your Namecheap API credentials:');
    console.log(`{
  "apiUser": "YOUR_NAMECHEAP_USERNAME",
  "apiKey": "YOUR_NAMECHEAP_API_KEY", 
  "ipAddress": "76.91.147.176",
  "sandbox": false
}`);
    process.exit(1);
}

// Load config
const config = JSON.parse(fs.readFileSync('./namecheap-config.json', 'utf8'));

// Validate config
if (!config.apiUser || !config.apiKey || config.apiUser === 'YOUR_NAMECHEAP_USERNAME') {
    console.error('❌ Please update namecheap-config.json with your actual Namecheap credentials');
    console.log('Get your API key from: https://ap.www.namecheap.com/settings/tools/apiaccess/');
    process.exit(1);
}

console.log('✅ Config loaded successfully');

// DNS records for Google App Engine
const dnsRecords = [
    // A records for IPv4
    { type: 'A', host: '@', value: '216.239.32.21', ttl: 3600 },
    { type: 'A', host: '@', value: '216.239.34.21', ttl: 3600 },
    { type: 'A', host: '@', value: '216.239.36.21', ttl: 3600 },
    { type: 'A', host: '@', value: '216.239.38.21', ttl: 3600 },
    
    // AAAA records for IPv6
    { type: 'AAAA', host: '@', value: '2001:4860:4802:32::15', ttl: 3600 },
    { type: 'AAAA', host: '@', value: '2001:4860:4802:34::15', ttl: 3600 },
    { type: 'AAAA', host: '@', value: '2001:4860:4802:36::15', ttl: 3600 },
    { type: 'AAAA', host: '@', value: '2001:4860:4802:38::15', ttl: 3600 },
    
    // CNAME for www
    { type: 'CNAME', host: 'www', value: 'ghs.googlehosted.com', ttl: 3600 }
];

// Set environment variables for Namecheap CLI
process.env.NAMECHEAP_API_USER = config.apiUser;
process.env.NAMECHEAP_API_KEY = config.apiKey;
process.env.NAMECHEAP_IP_ADDRESS = config.ipAddress;
process.env.NAMECHEAP_SANDBOX = config.sandbox ? 'true' : 'false';

try {
    console.log('🔍 Getting current DNS records...');
    
    // Get current DNS records
    const currentRecords = execSync('namecheap domains:dns:list hotppl.io', { encoding: 'utf8' });
    console.log('Current DNS records:', currentRecords);
    
    console.log('🗑️ Clearing existing DNS records...');
    
    // Clear existing records (optional - comment out if you want to keep existing records)
    // execSync('namecheap domains:dns:clear hotppl.io', { encoding: 'utf8' });
    
    console.log('➕ Adding new DNS records...');
    
    // Add each DNS record
    for (const record of dnsRecords) {
        try {
            const command = `namecheap domains:dns:add hotppl.io ${record.type} ${record.host} ${record.value} --ttl ${record.ttl}`;
            console.log(`Adding: ${record.type} ${record.host} → ${record.value}`);
            execSync(command, { encoding: 'utf8' });
            console.log(`✅ Added ${record.type} record`);
        } catch (error) {
            console.log(`⚠️ Warning: Could not add ${record.type} record (may already exist)`);
            console.log(error.message);
        }
    }
    
    console.log('🎉 DNS configuration complete!');
    console.log('');
    console.log('🌐 Your website will be available at:');
    console.log('   https://hotppl.io');
    console.log('   https://www.hotppl.io');
    console.log('');
    console.log('⏰ DNS propagation may take 15 minutes to 24 hours');
    console.log('🔒 SSL certificates are automatically managed by Google');
    
} catch (error) {
    console.error('❌ Error configuring DNS:', error.message);
    console.log('');
    console.log('💡 Manual setup instructions:');
    console.log('1. Go to Namecheap dashboard');
    console.log('2. Manage hotppl.io domain');
    console.log('3. Add these DNS records:');
    
    dnsRecords.forEach(record => {
        console.log(`   ${record.type} | ${record.host} | ${record.value}`);
    });
}
