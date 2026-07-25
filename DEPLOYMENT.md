# Deployment Guide

## Prerequisites

- Python 3.8+
- FFmpeg installed
- Git
- (Optional) Docker and Docker Compose

## Local Deployment

### 1. Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/file2vedio.git
cd file2vedio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
```

### 2. Configure

Edit `.env` with your settings:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-very-secure-secret-key-change-this
HOST=0.0.0.0
PORT=5000
TTS_VOICE=zh-CN-XiaoxiaoNeural
TTS_RATE=0.9
VIDEO_DURATION=180
VIDEO_WIDTH=1280
VIDEO_HEIGHT=720
```

### 3. Run

```bash
python app/main.py
```

Access at: **http://localhost:5000**

## Docker Deployment

### Option 1: Docker Compose (Recommended)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f file2vedio

# Stop
docker-compose down
```

### Option 2: Docker CLI

```bash
# Build image
docker build -t file2vedio:latest .

# Run container
docker run -d \
  --name file2vedio \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/output_videos:/app/output_videos \
  -e FLASK_ENV=production \
  file2vedio:latest

# View logs
docker logs -f file2vedio

# Stop container
docker stop file2vedio
docker rm file2vedio
```

## Production Deployment

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn (4 workers)
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'

# Run with Gunicorn (8 workers, suitable for production)
gunicorn -w 8 \
  --worker-class sync \
  --timeout 300 \
  -b 0.0.0.0:5000 \
  'app:create_app()'
```

### Using Nginx as Reverse Proxy

**nginx.conf:**

```nginx
upstream file2vedio {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://file2vedio;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

### SSL/HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d yourdomain.com

# Auto-renew
sudo systemctl enable certbot.timer
```

**Update nginx.conf:**

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## Systemd Service Setup

**Create `/etc/systemd/system/file2vedio.service`:**

```ini
[Unit]
Description=File2Vedio - Article to Video Generator
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/file2vedio
Environment="PATH=/var/www/file2vedio/venv/bin"
ExecStart=/var/www/file2vedio/venv/bin/gunicorn -w 8 -b 0.0.0.0:5000 'app:create_app()'
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
KillSignal=SIGQUIT
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable file2vedio
sudo systemctl start file2vedio
sudo systemctl status file2vedio
```

## Cloud Deployment

### Heroku

**Procfile:**

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT 'app:create_app()'
```

**Deploy:**

```bash
heroku create your-app-name
git push heroku main
heroku config:set FLASK_ENV=production
heroku open
```

### AWS EC2

```bash
# Launch instance
# Connect via SSH

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv ffmpeg nginx

# Clone and setup
git clone <repo-url>
cd file2vedio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Nginx (see above)
# Setup SSL with Let's Encrypt (see above)
# Create systemd service (see above)
```

### Google Cloud Run

**requirements.txt additions:**

```
gunicorn>=20.1.0
```

**Deploy:**

```bash
gcloud run deploy file2vedio \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Environment Variables

```env
# Server
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-secure-key>
HOST=0.0.0.0
PORT=5000

# Directories
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=output_videos
MAX_CONTENT_LENGTH=52428800  # 50MB

# Video Settings
VIDEO_DURATION=180  # 3 minutes
VIDEO_FPS=24
VIDEO_WIDTH=1280
VIDEO_HEIGHT=720
VIDEO_BITRATE=5000k

# TTS Settings
TTS_VOICE=zh-CN-XiaoxiaoNeural
TTS_RATE=0.9

# Subtitle Settings
SUBTITLE_FONT_SIZE=32
SUBTITLE_COLOR=ffffff
```

## Monitoring & Logging

### Application Logs

```bash
# Docker logs
docker-compose logs -f

# Systemd logs
journalctl -u file2vedio -f

# File logs (setup in app)
tail -f logs/app.log
```

### Health Monitoring

```bash
# Health check endpoint
curl http://localhost:5000/api/health

# Monitor with uptime monitoring service
# Configure external monitoring (e.g., Uptime Robot)
```

## Backup & Maintenance

### Backup Output Videos

```bash
# Backup to external storage
tar -czf file2vedio_videos_$(date +%Y%m%d).tar.gz output_videos/

# Upload to S3
aws s3 cp file2vedio_videos_*.tar.gz s3://your-bucket/backups/
```

### Cleanup Old Files

```bash
# Remove videos older than 30 days
find output_videos/ -type f -mtime +30 -delete

# Remove temp files
rm -rf temp/*
```

### Database Maintenance (if using)

```bash
# Backup database
pg_dump dbname > backup.sql

# Restore database
psql dbname < backup.sql
```

## Performance Optimization

### Caching

```bash
# Install Redis
sudo apt-get install redis-server

# Configure in app for session caching
```

### Load Balancing

For high traffic, use multiple Gunicorn instances behind a load balancer:

```bash
# Instance 1
gunicorn -w 4 -b 127.0.0.1:5000 'app:create_app()'

# Instance 2
gunicorn -w 4 -b 127.0.0.1:5001 'app:create_app()'

# Configure Nginx to balance load
upstream file2vedio {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
}
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>

# Or change PORT in .env
```

### Permission Denied

```bash
# Fix directory permissions
chmod -R 755 uploads/
chmod -R 755 output_videos/

# Change owner
sudo chown -R www-data:www-data /var/www/file2vedio
```

### Out of Disk Space

```bash
# Check disk usage
df -h

# Clean old videos
find output_videos/ -type f -mtime +7 -delete
```

## Security Checklist

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `FLASK_DEBUG=False` in production
- [ ] Use HTTPS/SSL in production
- [ ] Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- [ ] Set up proper file permissions
- [ ] Configure firewall rules
- [ ] Setup regular backups
- [ ] Enable CORS only for trusted origins
- [ ] Implement rate limiting
- [ ] Monitor logs for suspicious activity

## Support

For deployment issues, please:
1. Check logs for error messages
2. Review this guide
3. Open a GitHub issue with error details
