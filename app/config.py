import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Upload Settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 52428800))  # 50MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', 'output_videos')
    TEMP_FOLDER = 'temp'
    
    # Video Generation
    VIDEO_DURATION = int(os.getenv('VIDEO_DURATION', 180))  # 3 minutes
    VIDEO_FPS = int(os.getenv('VIDEO_FPS', 24))
    VIDEO_WIDTH = int(os.getenv('VIDEO_WIDTH', 1280))
    VIDEO_HEIGHT = int(os.getenv('VIDEO_HEIGHT', 720))
    VIDEO_BITRATE = '5000k'
    
    # TTS Settings
    TTS_VOICE = os.getenv('TTS_VOICE', 'zh-CN-XiaoxiaoNeural')
    TTS_RATE = float(os.getenv('TTS_RATE', 0.9))
    
    # Subtitle Settings
    SUBTITLE_FONT_SIZE = int(os.getenv('SUBTITLE_FONT_SIZE', 32))
    SUBTITLE_COLOR = os.getenv('SUBTITLE_COLOR', 'ffffff')
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))