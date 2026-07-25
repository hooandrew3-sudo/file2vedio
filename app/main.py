from app import create_app
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    app = create_app()
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', True)
    
    print(f"\n{'='*50}")
    print(f"🎬 File2Vedio - Article to Video Generator")
    print(f"{'='*50}")
    print(f"Starting server at http://{host}:{port}")
    print(f"API Documentation at http://{host}:{port}/api/health")
    print(f"{'='*50}\n")
    
    app.run(host=host, port=port, debug=debug)