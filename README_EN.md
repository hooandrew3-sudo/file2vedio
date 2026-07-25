# File2Vedio

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Framework-Flask-blue)](https://flask.palletsprojects.com/)

🎬 **Convert articles into beautiful 3-minute anime-style videos with AI voiceover, subtitles, and MP4 export.**

## ✨ Features

✅ **Intelligent Article Processing**
- Automatic content extraction and compression
- Adaptive text segmentation for natural speech
- Support for multiple languages (Chinese, English, Japanese, Korean)

✅ **AI Voice Generation**
- Multiple natural female voices powered by Microsoft Edge TTS
- Customizable speech rate and emotional intonation
- Support for different languages and accents

✅ **Professional Subtitles**
- Automatic SRT/VTT subtitle generation
- Real-time synchronization with audio
- Customizable font, size, and colors

✅ **Anime-Style Backgrounds**
- Dynamic 2D scene rendering
- Multiple color schemes and themes
- Smooth animations and transitions

✅ **High-Quality Video Output**
- 1280x720 resolution (adjustable)
- MP4 format for universal compatibility
- Optimized bitrate for balance between quality and size

✅ **Easy-to-Use Interface**
- Beautiful web UI for non-technical users
- REST API for developers
- Real-time progress tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- FFmpeg installed
- Internet connection (for TTS)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/file2vedio.git
cd file2vedio

# Run setup (Linux/macOS)
chmod +x install.sh
./install.sh

# Or manual setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Run

```bash
python app/main.py
```

Visit: **http://localhost:5000**

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Deployment Guide](DEPLOYMENT.md)** - Deploy to production
- **[API Examples](API_EXAMPLES.md)** - Use the REST API
- **[Contributing Guide](CONTRIBUTING.md)** - Contribute to the project
- **[Project Status](PROJECT_STATUS.md)** - Features and roadmap

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Voice Synthesis**: Microsoft Edge TTS
- **Video Processing**: FFmpeg, moviepy
- **Image Rendering**: OpenCV, Pillow
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Containerization**: Docker & Docker Compose

## 📖 Usage Example

### Web Interface

1. Open http://localhost:5000
2. Enter article title and content
3. Select voice (optional)
4. Click "Generate Video"
5. Download MP4 when ready

### REST API

```python
import requests

# Upload article
response = requests.post('http://localhost:5000/api/upload', json={
    'title': 'My Article',
    'content': 'Article content here...'
})

task_id = response.json()['task_id']

# Check status
status = requests.get(f'http://localhost:5000/api/status/{task_id}').json()
print(f"Progress: {status['progress']}%")

# Download video
video = requests.get(f'http://localhost:5000/api/download/{task_id}')
with open('video.mp4', 'wb') as f:
    f.write(video.content)
```

## 🐳 Docker Deployment

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Using Docker CLI
docker build -t file2vedio .
docker run -d -p 5000:5000 file2vedio
```

## ⚙️ Configuration

Edit `.env` to customize:

```env
# Server
HOST=0.0.0.0
PORT=5000

# Video Settings
VIDEO_DURATION=180      # 3 minutes
VIDEO_WIDTH=1280
VIDEO_HEIGHT=720

# Voice Settings
TTS_VOICE=zh-CN-XiaoxiaoNeural  # Female voice
TTS_RATE=0.9                     # Speech speed (0.5-2.0)
```

## 📊 Project Structure

```
file2vedio/
├── app/
│   ├── modules/           # Core functionality
│   │   ├── text_processor.py      # Text extraction & processing
│   │   ├── tts_engine.py          # Voice synthesis
│   │   ├── subtitle_handler.py    # Subtitle generation
│   │   ├── video_generator.py     # Video composition
│   │   └── anime_renderer.py      # Background rendering
│   ├── routes/
│   │   ├── api.py         # REST API endpoints
│   │   └── web.py         # Web interface
│   ├── templates/
│   │   └── index.html     # Web UI
│   ├── static/
│   │   ├── css/style.css  # Styling
│   │   └── js/app.js      # Frontend logic
│   ├── __init__.py        # App factory
│   └── main.py            # Entry point
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image
├── docker-compose.yml     # Docker Compose config
├── Makefile               # Development commands
└── README.md              # This file
```

## 🔄 Processing Pipeline

1. **Text Processing** → Extract key content, compress to 3 minutes
2. **Voice Synthesis** → Generate natural female voiceover
3. **Subtitle Generation** → Create synchronized subtitles
4. **Background Rendering** → Generate anime-style scenes
5. **Video Composition** → Combine audio, video, and subtitles
6. **MP4 Export** → Package as downloadable video

## 🎯 API Endpoints

### POST /api/upload
Upload article and start video generation

```json
{
  "title": "Article Title",
  "content": "Article content..."
}
```

### GET /api/status/<task_id>
Check video generation progress

### GET /api/download/<task_id>
Download generated MP4 video

### GET /api/voices
List available TTS voices

### GET /api/health
Health check endpoint

## 🐛 Troubleshooting

**FFmpeg not found**
```bash
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # macOS
```

**Port already in use**
- Change `PORT` in `.env` file
- Or kill the process: `lsof -i :5000 | kill -9 <PID>`

**TTS fails**
- Check internet connection
- Try a different voice in `.env`
- Check logs for error messages

## 📈 Performance Tips

- Reduce video resolution for faster generation
- Lower bitrate in `.env` (trade-off: quality vs. size)
- Use GPU acceleration if available
- Deploy behind Nginx for better load handling

## 🚀 Production Deployment

For production use:
1. Use Gunicorn or uWSGI
2. Set up Nginx reverse proxy
3. Enable SSL/HTTPS
4. Configure firewall rules
5. Set up monitoring and logging
6. Implement rate limiting

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📝 Roadmap

- [ ] Async task processing with Celery
- [ ] Database integration
- [ ] User authentication
- [ ] Video templates
- [ ] Background music
- [ ] Batch processing
- [ ] Video editing tools
- [ ] Mobile app

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 💬 Support

- 📖 [Documentation](QUICKSTART.md)
- 🐛 [Report Issues](https://github.com/yourusername/file2vedio/issues)
- 💡 [Feature Requests](https://github.com/yourusername/file2vedio/discussions)

## 🙏 Acknowledgments

- Microsoft Edge TTS for voice synthesis
- FFmpeg for video processing
- Flask community for excellent framework
- All contributors and users

---

**Made with ❤️ for content creators and developers**

⭐ If you find this project helpful, please consider giving it a star!
