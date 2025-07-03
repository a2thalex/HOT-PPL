// Test navigation flow for HOT PPL website
const https = require('https');

async function testURL(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                resolve({
                    url: url,
                    status: res.statusCode,
                    hasContent: data.length > 0,
                    title: data.match(/<title>(.*?)<\/title>/)?.[1] || 'No title'
                });
            });
        }).on('error', reject);
    });
}

async function testNavigation() {
    console.log('🧪 Testing HOT PPL website navigation...\n');
    
    const urls = [
        'https://hotppl.io',
        'https://hotppl.io/scenes',
        'https://hotppl.io/create',
        'https://hotppl.io/submit',
        'https://hotppl.io/confirmation'
    ];
    
    for (const url of urls) {
        try {
            const result = await testURL(url);
            const status = result.status === 200 ? '✅' : '❌';
            console.log(`${status} ${result.url}`);
            console.log(`   Status: ${result.status}`);
            console.log(`   Title: ${result.title}`);
            console.log('');
        } catch (error) {
            console.log(`❌ ${url}`);
            console.log(`   Error: ${error.message}`);
            console.log('');
        }
    }
    
    console.log('🎯 Navigation test complete!');
}

testNavigation();
