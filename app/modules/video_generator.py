import os
import logging
from typing import List, Dict, Optional
import subprocess
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips
import numpy as np

logger = logging.getLogger(__name__)

class VideoGenerator:
    """
    Generate video from audio and background images
    """
    
    def __init__(self, width: int = 1280, height: int = 720, fps: int = 24, bitrate: str = '5000k'):
        """
        Initialize video generator
        
        Args:
            width: Video width in pixels
            height: Video height in pixels
            fps: Frames per second
            bitrate: Video bitrate (e.g., '5000k')
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.bitrate = bitrate
    
    def create_video_from_audio_and_image(
        self,
        audio_path: str,
        background_image: str,
        output_path: str
    ) -> bool:
        """
        Create video from audio and static background image
        
        Args:
            audio_path: Path to audio file
            background_image: Path to background image
            output_path: Path to save video file
        
        Returns:
            True if successful
        """
        try:
            # Get audio duration
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Create video using ffmpeg
            cmd = [
                'ffmpeg',
                '-loop', '1',
                '-i', background_image,
                '-i', audio_path,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-shortest',
                '-pix_fmt', 'yuv420p',
                '-preset', 'medium',
                '-b:v', self.bitrate,
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Video created successfully: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Video creation failed: {str(e)}")
            return False
    
    def create_video_from_images_and_audio(
        self,
        image_paths: List[str],
        audio_path: str,
        output_path: str,
        display_duration: float = 3.0
    ) -> bool:
        """
        Create video from multiple images and audio
        
        Args:
            image_paths: List of image file paths
            audio_path: Path to audio file
            output_path: Path to save video file
            display_duration: Duration to display each image (seconds)
        
        Returns:
            True if successful
        """
        try:
            audio = AudioFileClip(audio_path)
            total_duration = audio.duration
            
            # Create image list for concat
            image_list = []
            image_index = 0
            current_time = 0
            
            while current_time < total_duration:
                image_path = image_paths[image_index % len(image_paths)]
                image_list.append(image_path)
                
                current_time += display_duration
                image_index += 1
            
            # Create temp image list file
            concat_file = '/tmp/concat_images.txt'
            with open(concat_file, 'w') as f:
                for img in image_list:
                    duration = min(display_duration, total_duration - (image_list.index(img) * display_duration))
                    f.write(f"file '{img}'\n")
                    f.write(f"duration {duration}\n")
            
            # Use ffmpeg to create video
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_file,
                '-i', audio_path,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-pix_fmt', 'yuv420p',
                '-vsync', 'vfr',
                '-preset', 'medium',
                '-b:v', self.bitrate,
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Video created from images: {output_path}")
            
            # Clean up temp file
            os.remove(concat_file)
            return True
        
        except Exception as e:
            logger.error(f"Video creation from images failed: {str(e)}")
            return False
    
    def merge_audio_video(
        self,
        video_path: str,
        audio_path: str,
        output_path: str
    ) -> bool:
        """
        Replace or merge audio with video
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_path: Path to save merged video
        
        Returns:
            True if successful
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-shortest',
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Audio merged successfully: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Audio merge failed: {str(e)}")
            return False