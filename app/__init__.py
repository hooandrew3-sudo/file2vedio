from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    CORS(app)
    
    # Configuration
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 52428800))
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    app.config['OUTPUT_FOLDER'] = os.getenv('OUTPUT_FOLDER', 'output_videos')
    
    # Create directories if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs('temp', exist_ok=True)
    
    logger.info(f"Upload folder: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")
    logger.info(f"Output folder: {os.path.abspath(app.config['OUTPUT_FOLDER'])}")
    
    # Register blueprints
    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app