#!/bin/bash
# Deploy to Cloudflare

set -e

echo "🚀 Deploying File2Vedio to Cloudflare..."
echo ""

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "❗ Installing Wrangler CLI..."
    npm install -g wrangler
fi

# Login to Cloudflare
echo "🔐 Authenticating with Cloudflare..."
wrangler login

# Build the application
echo "🔷 Building application..."
npm install
npm run build

# Deploy to Cloudflare Pages
echo "🚀 Deploying to Cloudflare Pages..."
wrangler pages deploy dist/

# Deploy Workers
echo "🚀 Deploying Workers..."
wrangler deploy

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Your site is now live at:"
echo "   https://file2vedio.pages.dev"
echo ""
echo "💾 Environment: Production"
echo "💾 Region: Global (Cloudflare CDN)"
echo ""
