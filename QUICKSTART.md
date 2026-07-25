# Quick Start Guide

## Installation

### Automated Setup (Linux/macOS)

```bash
chmod +x install.sh
./install.sh
```

### Manual Setup

1. **Install FFmpeg** (required)

```bash
# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from: https://ffmpeg.org/download.html
```

2. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment**

```bash
cp .env.example .env
# Edit .env file as needed
```

## Running the Application

```bash
python app/main.py
```

Then visit: **http://localhost:5000**

## Usage

### Web Interface

1. Enter article title
2. Paste or type article content
3. Select voice (optional)
4. Click "Generate Video"
5. Wait for processing
6. Download MP4 file

### Using the API

#### Upload and generate video

```bash
curl -X POST http://localhost:5000/api/upload \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Article",
    "content": "Article text here..."
  }'
```

Response:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing"
}
```

#### Check status

```bash
curl http://localhost:5000/api/status/550e8400-e29b-41d4-a716-446655440000
```

Response:
```json
{
  "status": "completed",
  "progress": 100,
  "title": "My Article",
  "error": null
}
```

#### Download video

```bash
curl -O http://localhost:5000/api/download/550e8400-e29b-41d4-a716-446655440000
```

## Features

✅ **Article Processing**
- Automatic content extraction
- Compression to 3 minutes
- Sentence segmentation

✅ **Voice Generation**
- Multiple female voices
- Customizable speech rate
- Natural intonation

✅ **Subtitle Support**
- SRT format
- Automatic timing sync
- Customizable styling

✅ **Anime-style Backgrounds**
- Multiple color schemes
- Dynamic rendering
- Customizable animations

✅ **Video Output**
- MP4 format
- 1280x720 resolution (adjustable)
- Quality bitrate: 5000k

## Configuration

Edit `.env` file to customize:

```env
# Server
HOST=0.0.0.0
PORT=5000
FLASK_DEBUG=True

# Video Settings
VIDEO_DURATION=180          # 3 minutes
VIDEO_FPS=24
VIDEO_WIDTH=1280
VIDEO_HEIGHT=720

# TTS Settings
TTS_VOICE=zh-CN-XiaoxiaoNeural  # Female voice
TTS_RATE=0.9                     # Speed (0.5-2.0)

# Subtitle Settings
SUBTITLE_FONT_SIZE=32
SUBTITLE_COLOR=ffffff           # White
```

## Troubleshooting

### FFmpeg not found
```bash
# Install FFmpeg
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # macOS
```

### TTS fails to generate audio
- Check internet connection
- Try different voice: `zh-TW-HsiaoChenNeural`, `en-US-AriaNeural`
- Check logs for detailed error messages

### Video generation is slow
- Reduce video resolution in `.env`
- Lower bitrate (e.g., `3000k`)
- Use GPU acceleration if available

### Port already in use
```bash
# Change PORT in .env
PORT=8000
```

## Development

### Project Structure
```
file2vedio/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── main.py              # Entry point
│   ├── modules/             # Core functionality
│   │   ├── text_processor.py
│   │   ├── tts_engine.py
│   │   ├── subtitle_handler.py
│   │   ├── video_generator.py
│   │   └── anime_renderer.py
│   ├── routes/              # API routes
│   │   ├── api.py           # REST API
│   │   └── web.py           # Web interface
│   ├── templates/           # HTML templates
│   │   └── index.html
│   └── static/              # CSS/JS
│       ├── css/style.css
│       └── js/app.js
├── uploads/                 # Input files
├── output_videos/           # Generated videos
├── requirements.txt         # Python dependencies
└── .env.example            # Environment template
```

## Performance Tips

1. **For Production Deployment**
   - Use Gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'`
   - Use Celery for async task processing
   - Set up Redis for task queue
   - Deploy behind Nginx

2. **Optimize Video Quality**
   - Adjust `VIDEO_BITRATE` based on target quality
   - Use hardware encoding if GPU available
   - Enable ffmpeg caching

3. **Speed Up Processing**
   - Reduce `VIDEO_WIDTH` and `VIDEO_HEIGHT`
   - Use `libx265` codec (slower encode, better quality)
   - Implement frame pre-caching

## License

MIT License - Feel free to use and modify

## Support

For issues and questions, please open a GitHub issue.
