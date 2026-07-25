import os
import sys
from app import create_app
from app.routes.web import web_bp
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app = create_app()
    
    # Register web blueprint
    app.register_blueprint(web_bp)
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"🎬 File2Vedio - Article to Video Generator")
    print(f"{'='*60}")
    print(f"\n✨ Starting server...")
    print(f"   Web Interface: http://{host}:{port}")
    print(f"   API Docs: http://{host}:{port}/api/health")
    print(f"   Debug Mode: {debug}")
    print(f"\n💾 Configuration:")
    print(f"   Max Upload Size: {os.getenv('MAX_CONTENT_LENGTH', 52428800)} bytes")
    print(f"   Video Duration: {os.getenv('VIDEO_DURATION', 180)} seconds")
    print(f"   TTS Voice: {os.getenv('TTS_VOICE', 'zh-CN-XiaoxiaoNeural')}")
    print(f"   TTS Rate: {os.getenv('TTS_RATE', 0.9)}")
    print(f"\n{'='*60}\n")
    
    try:
        app.run(host=host, port=port, debug=debug, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1)