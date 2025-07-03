# HOT PPL DNS Setup Script for Namecheap
# Configure DNS records for hotppl.io to point to Google App Engine

Write-Host "🌐 Setting up DNS for hotppl.io..." -ForegroundColor Cyan

# Check if config file exists
if (-not (Test-Path "namecheap-config.json")) {
    Write-Host "❌ namecheap-config.json not found!" -ForegroundColor Red
    Write-Host "Please update namecheap-config.json with your Namecheap API credentials" -ForegroundColor Yellow
    Write-Host "Get your API key from: https://ap.www.namecheap.com/settings/tools/apiaccess/" -ForegroundColor Yellow
    exit 1
}

# Load config
$config = Get-Content "namecheap-config.json" | ConvertFrom-Json

# Validate config
if ($config.apiUser -eq "YOUR_NAMECHEAP_USERNAME" -or -not $config.apiKey) {
    Write-Host "❌ Please update namecheap-config.json with your actual credentials" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Config loaded successfully" -ForegroundColor Green

# Set environment variables
$env:NAMECHEAP_API_USER = $config.apiUser
$env:NAMECHEAP_API_KEY = $config.apiKey
$env:NAMECHEAP_IP_ADDRESS = $config.ipAddress
$env:NAMECHEAP_SANDBOX = if ($config.sandbox) { "true" } else { "false" }

# DNS records for Google App Engine
$dnsRecords = @(
    @{ type = "A"; host = "@"; value = "216.239.32.21"; ttl = 3600 },
    @{ type = "A"; host = "@"; value = "216.239.34.21"; ttl = 3600 },
    @{ type = "A"; host = "@"; value = "216.239.36.21"; ttl = 3600 },
    @{ type = "A"; host = "@"; value = "216.239.38.21"; ttl = 3600 },
    @{ type = "AAAA"; host = "@"; value = "2001:4860:4802:32::15"; ttl = 3600 },
    @{ type = "AAAA"; host = "@"; value = "2001:4860:4802:34::15"; ttl = 3600 },
    @{ type = "AAAA"; host = "@"; value = "2001:4860:4802:36::15"; ttl = 3600 },
    @{ type = "AAAA"; host = "@"; value = "2001:4860:4802:38::15"; ttl = 3600 },
    @{ type = "CNAME"; host = "www"; value = "ghs.googlehosted.com"; ttl = 3600 }
)

try {
    Write-Host "🔍 Getting current DNS records..." -ForegroundColor Yellow
    
    # Get current DNS records
    $currentRecords = & namecheap domains:dns:list hotppl.io 2>&1
    Write-Host "Current DNS records: $currentRecords" -ForegroundColor Gray
    
    Write-Host "➕ Adding new DNS records..." -ForegroundColor Yellow
    
    # Add each DNS record
    foreach ($record in $dnsRecords) {
        try {
            Write-Host "Adding: $($record.type) $($record.host) → $($record.value)" -ForegroundColor Cyan
            & namecheap domains:dns:add hotppl.io $record.type $record.host $record.value --ttl $record.ttl 2>&1
            Write-Host "✅ Added $($record.type) record" -ForegroundColor Green
        }
        catch {
            Write-Host "⚠️ Warning: Could not add $($record.type) record (may already exist)" -ForegroundColor Yellow
        }
    }
    
    Write-Host ""
    Write-Host "🎉 DNS configuration complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Your website will be available at:" -ForegroundColor Cyan
    Write-Host "   https://hotppl.io" -ForegroundColor White
    Write-Host "   https://www.hotppl.io" -ForegroundColor White
    Write-Host ""
    Write-Host "⏰ DNS propagation may take 15 minutes to 24 hours" -ForegroundColor Yellow
    Write-Host "🔒 SSL certificates are automatically managed by Google" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error configuring DNS: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Manual setup instructions:" -ForegroundColor Yellow
    Write-Host "1. Go to Namecheap dashboard" -ForegroundColor White
    Write-Host "2. Manage hotppl.io domain" -ForegroundColor White
    Write-Host "3. Add these DNS records:" -ForegroundColor White
    
    foreach ($record in $dnsRecords) {
        Write-Host "   $($record.type) | $($record.host) | $($record.value)" -ForegroundColor Gray
    }
}
