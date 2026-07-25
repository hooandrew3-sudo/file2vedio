# Cloudflare Deployment Guide

## Prerequisites

- Cloudflare account
- Wrangler CLI installed: `npm install -g wrangler`
- GitHub repository connected to Cloudflare

## Setup Steps

### 1. Create Cloudflare Account & Setup

```bash
# Login to Cloudflare
wrangler login

# Verify authentication
wrangler whoami
```

### 2. Create R2 Bucket for Video Storage

```bash
# Create bucket for production
wrangler r2 bucket create file2vedio-videos

# Create bucket for staging
wrangler r2 bucket create file2vedio-videos-preview

# List buckets
wrangler r2 bucket list
```

### 3. Create Durable Objects for Task Management

Edit `wrangler.toml`:

```toml
[[durable_objects.bindings]]
name = "TASK_QUEUE"
class_name = "TaskQueue"
script_name = "file2vedio-worker"
```

### 4. Setup KV Namespace for Caching

```bash
# Create KV namespace for production
wrangler kv:namespace create "CACHE"

# Create KV namespace for preview
wrangler kv:namespace create "CACHE" --preview
```

### 5. Deploy to Cloudflare Pages

#### Option A: Using GitHub Integration

1. Go to Cloudflare Dashboard → Pages
2. Click "Create a project"
3. Select "Connect to Git"
4. Choose GitHub repository
5. Configure build settings:
   - Framework: None
   - Build command: `npm install && npm run build`
   - Build output directory: `dist`
6. Click "Save and Deploy"

#### Option B: Using Wrangler CLI

```bash
# Deploy to Pages
wrangler pages deploy dist/

# Deploy to specific environment
wrangler pages deploy dist/ --project-name file2vedio --branch main
```

### 6. Configure Domain

1. In Cloudflare Dashboard → Pages → file2vedio
2. Go to "Custom domains"
3. Add your domain (e.g., file2vedio.com)
4. Update DNS records if needed

## Architecture

```
┌─────────────────────────────────────────┐
│         User Browser                    │
│      (file2vedio.com)                   │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼─────────┐
        │  Cloudflare CDN  │
        │   (Global Edge)  │
        └────────┬─────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼────┐  ┌───▼────┐  ┌───▼────┐
│ Pages  │  │Workers │  │ R2     │
│(Static)│  │(API)   │  │(Videos)│
└────────┘  └────────┘  └────────┘
```

## Environment Variables

Set in Cloudflare Dashboard → Pages → Settings → Environment variables:

```
API_ENDPOINT=https://api.file2vedio.com
PYTHON_BACKEND_URL=https://python-api.file2vedio.com
R2_BUCKET_NAME=file2vedio-videos
R2_ACCOUNT_ID=your-account-id
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
TTS_API_KEY=your-edge-tts-key
```

## Routing Configuration

Create `_routes.json` for proper routing:

```json
{
  "routes": [
    {
      "pattern": "file2vedio.com/api/*",
      "zone_name": "file2vedio.com"
    },
    {
      "pattern": "file2vedio.com/download/*",
      "zone_name": "file2vedio.com"
    },
    {
      "pattern": "file2vedio.com/status/*",
      "zone_name": "file2vedio.com"
    }
  ]
}
```

## Performance Optimization

### 1. Enable Caching

In Cloudflare Dashboard:
- Go to Caching → Cache Rules
- Create rule to cache API responses (5 minutes)
- Set TTL for static assets (1 year)

### 2. Setup Rate Limiting

```
Go to Security → Rate limiting
Create rules:
- API endpoint: 100 requests/minute
- Upload endpoint: 10 requests/minute
```

### 3. Enable Image Optimization

```
Go to Speed → Image Optimization
Enable: Polish, Mirage, WebP
```

## Monitoring

### 1. Analytics

Cloudflare Dashboard → Analytics
- Page views
- Request rate
- Error rate
- Cache hit ratio

### 2. Real-time Logs

```bash
# Stream real-time logs
wrangler tail

# Filter by status code
wrangler tail --status 500
```

### 3. Setup Alerts

Dashboard → Notifications → Alert Policies
- High error rate (>5%)
- Service down
- SSL certificate expiring

## CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/deploy-cloudflare.yml`:

```yaml
name: Deploy to Cloudflare

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Build
        run: npm run build
      
      - name: Deploy to Cloudflare
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

## Troubleshooting

### 1. 502 Bad Gateway

- Check if backend API is accessible
- Verify CORS headers
- Check Cloudflare firewall rules

```bash
# Test connectivity
curl -i https://your-backend-url/api/health
```

### 2. Slow Performance

- Check cache hit ratio
- Enable image optimization
- Use regional endpoints
- Monitor Worker CPU time

```bash
# Check Worker performance
wrangler publish --dry-run
```

### 3. Upload Failures

- Check R2 bucket permissions
- Verify API credentials
- Check request size limits (100MB max)
- Monitor bandwidth usage

## Security Best Practices

1. **API Keys**: Store in Cloudflare Secrets, never commit
2. **Rate Limiting**: Prevent abuse and DDoS
3. **CORS**: Configure properly to allow only trusted origins
4. **WAF**: Enable Cloudflare WAF rules
5. **SSL/TLS**: Use "Full (strict)" mode
6. **DDoS Protection**: Enable advanced DDoS protection

## Backup & Recovery

### Backup R2 Bucket

```bash
# List all files
wrangler r2 object list file2vedio-videos

# Download backup
wrangler r2 object download file2vedio-videos/backup.tar.gz > backup.tar.gz
```

### Restore from Backup

```bash
# Upload backup files
wrangler r2 object create file2vedio-videos/backup.tar.gz < backup.tar.gz
```

## Cost Optimization

- **Pages**: Free tier (500 deployments/month)
- **Workers**: Free tier (100k requests/day)
- **R2**: $0.015/GB storage, $0.015/million operations
- **KV**: Free tier (100k ops/day)

## Migration from Local Deployment

### 1. Export Videos

```bash
# Sync local videos to R2
wrangler r2 sync output_videos/ file2vedio-videos/ --delete
```

### 2. Migrate Database (if applicable)

```bash
# Export from local
pg_dump dbname > backup.sql

# Import to Cloudflare D1 (SQL database)
wrangler d1 execute db < backup.sql
```

### 3. Update DNS

- Point domain to Cloudflare nameservers
- Configure DNS records
- Enable proxying (orange cloud)

## Support

- Cloudflare Documentation: https://developers.cloudflare.com
- Community: https://community.cloudflare.com
- Status Page: https://www.cloudflarestatus.com
