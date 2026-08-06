#!/bin/bash

# 🚀 Quick Deploy Script for Cloudflare Workers
# Run this script to deploy file2video to Cloudflare

set -e

echo "================================"
echo "🚀 file2video Cloudflare Deploy"
echo "================================"
echo ""

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler CLI not found. Installing..."
    npm install -g @wrangler/cli
fi

# Check authentication
echo "🔐 Checking Cloudflare authentication..."
if ! wrangler whoami &> /dev/null; then
    echo "❌ Not authenticated. Running: wrangler login"
    wrangler login
fi

ACCOUNT_ID=$(wrangler whoami | grep -oP 'Account ID: \K.*' || echo "")
if [ -z "$ACCOUNT_ID" ]; then
    echo "❌ Could not get Account ID. Please run: wrangler whoami"
    exit 1
fi

echo "✅ Account ID: $ACCOUNT_ID"
echo ""

# Update wrangler.toml with account ID
echo "📝 Updating wrangler.toml..."
sed -i.bak "s/account_id = \".*\"/account_id = \"$ACCOUNT_ID\"/" wrangler.toml
rm -f wrangler.toml.bak

echo "✅ wrangler.toml updated"
echo ""

# Create R2 buckets
echo "🪣 Creating R2 buckets..."

if wrangler r2 bucket list | grep -q "file2video-uploads"; then
    echo "✅ Bucket 'file2video-uploads' already exists"
else
    echo "📦 Creating 'file2video-uploads'..."
    wrangler r2 bucket create file2video-uploads
fi

if wrangler r2 bucket list | grep -q "file2video-videos"; then
    echo "✅ Bucket 'file2video-videos' already exists"
else
    echo "📦 Creating 'file2video-videos'..."
    wrangler r2 bucket create file2video-videos
fi

echo ""

# List buckets
echo "🪣 R2 Buckets:"
wrangler r2 bucket list

echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

echo "✅ Dependencies installed"
echo ""

# Build project
echo "🔨 Building project..."
npm run build 2>/dev/null || echo "⚠️  No build script defined"

echo ""

# Deploy to Cloudflare
echo "🚀 Deploying to Cloudflare..."
wrangler deploy --env production

echo ""
echo "================================"
echo "✅ Deployment Complete!"
echo "================================"
echo ""

# Get deployment URL
WORKER_URL=$(wrangler deployments list | head -2 | tail -1 | awk '{print $2}' 2>/dev/null || echo "your-worker.workers.dev")

echo "📍 Your Worker URL:"
echo "   https://$WORKER_URL"
echo ""

echo "🎬 Access your app:"
echo "   https://$WORKER_URL"
echo ""

echo "📊 Monitor logs:"
echo "   wrangler tail"
echo ""

echo "🔄 Rollback (if needed):"
echo "   wrangler rollback"
echo ""

echo "Happy video converting! 🎉"
