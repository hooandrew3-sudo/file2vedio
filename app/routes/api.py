from flask import Blueprint, request, jsonify, send_file, current_app
import os
import uuid
from datetime import datetime
import logging
from app.modules import (
    TextProcessor,
    TTSEngine,
    SubtitleHandler,
    VideoGenerator,
    AnimeRenderer
)

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)

# In-memory task status tracking (use database in production)
task_status = {}

@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@api_bp.route('/upload', methods=['POST'])
def upload_article():
    """
    Upload article and start video generation
    Expected JSON: {"title": "...", "content": "..."}
    """
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400
        
        title = data.get('title', 'Untitled')
        content = data.get('content', '')
        
        # Create task ID
        task_id = str(uuid.uuid4())
        
        # Initialize task status
        task_status[task_id] = {
            'status': 'processing',
            'title': title,
            'progress': 0,
            'created_at': datetime.now().isoformat(),
            'error': None
        }
        
        # Process in background (simplified - would use Celery in production)
        try:
            video_path = generate_video_from_content(task_id, title, content)
            
            if video_path:
                task_status[task_id]['status'] = 'completed'
                task_status[task_id]['progress'] = 100
                task_status[task_id]['video_path'] = video_path
            else:
                task_status[task_id]['status'] = 'failed'
                task_status[task_id]['error'] = 'Video generation failed'
        except Exception as e:
            task_status[task_id]['status'] = 'failed'
            task_status[task_id]['error'] = str(e)
            logger.error(f"Error generating video for task {task_id}: {str(e)}")
        
        return jsonify({'task_id': task_id, 'status': 'processing'}), 202
    
    except Exception as e:
        logger.error(f"Upload endpoint error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """
    Get status of video generation task
    """
    if task_id not in task_status:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task_status[task_id]), 200

@api_bp.route('/download/<task_id>', methods=['GET'])
def download_video(task_id):
    """
    Download generated video
    """
    if task_id not in task_status:
        return jsonify({'error': 'Task not found'}), 404
    
    status = task_status[task_id]
    
    if status['status'] != 'completed':
        return jsonify({'error': f"Task not completed. Current status: {status['status']}"}), 400
    
    video_path = status.get('video_path')
    
    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found'}), 404
    
    return send_file(video_path, as_attachment=True, download_name=f"{status['title']}.mp4")

@api_bp.route('/voices', methods=['GET'])
def get_available_voices():
    """
    Get available TTS voices
    """
    voices = TTSEngine.get_available_voices()
    return jsonify({'voices': voices}), 200

def generate_video_from_content(task_id: str, title: str, content: str) -> str:
    """
    Generate video from article content
    
    Args:
        task_id: Unique task identifier
        title: Article title
        content: Article content
    
    Returns:
        Path to generated video file
    """
    temp_dir = os.path.join(current_app.config['TEMP_FOLDER'], task_id)
    output_dir = current_app.config['OUTPUT_FOLDER']
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Step 1: Process text
        text_processor = TextProcessor(max_duration=180)
        processed_text = text_processor.extract_key_content(content)
        script = text_processor.generate_script(processed_text)
        
        task_status[task_id]['progress'] = 10
        
        # Step 2: Generate speech
        tts_engine = TTSEngine(voice='zh-CN-XiaoxiaoNeural', rate=0.9)
        audio_path = os.path.join(temp_dir, 'audio.mp3')
        
        if not tts_engine.synthesize(processed_text, audio_path):
            raise Exception("TTS synthesis failed")
        
        task_status[task_id]['progress'] = 40
        
        # Step 3: Generate subtitles
        subtitle_handler = SubtitleHandler(font_size=32, color='ffffff')
        subtitle_path = os.path.join(temp_dir, 'subtitles.srt')
        subtitle_handler.generate_subtitles_srt(script['segments'], subtitle_path)
        
        task_status[task_id]['progress'] = 60
        
        # Step 4: Create anime background
        anime_renderer = AnimeRenderer(width=1280, height=720)
        background_path = os.path.join(temp_dir, 'background.png')
        anime_renderer.create_anime_background(background_path, color_scheme='cool')
        
        task_status[task_id]['progress'] = 75
        
        # Step 5: Generate video
        video_generator = VideoGenerator(width=1280, height=720, fps=24)
        video_path = os.path.join(temp_dir, 'video.mp4')
        
        if not video_generator.create_video_from_audio_and_image(audio_path, background_path, video_path):
            raise Exception("Video generation failed")
        
        task_status[task_id]['progress'] = 90
        
        # Step 6: Embed subtitles
        final_video_path = os.path.join(output_dir, f"{task_id}.mp4")
        if not subtitle_handler.embed_subtitles_in_video(video_path, subtitle_path, final_video_path):
            # Fallback: use video without embedded subtitles
            import shutil
            shutil.copy(video_path, final_video_path)
        
        task_status[task_id]['progress'] = 100
        logger.info(f"Video generated successfully for task {task_id}: {final_video_path}")
        
        return final_video_path
    
    except Exception as e:
        logger.error(f"Error in generate_video_from_content: {str(e)}")
        raise