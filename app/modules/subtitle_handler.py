import os
from typing import List, Dict, Tuple
from datetime import timedelta
import re

class SubtitleHandler:
    """
    Generate and manage subtitles (SRT/VTT format)
    """
    
    def __init__(self, font_size: int = 32, color: str = 'ffffff'):
        """
        Initialize subtitle handler
        
        Args:
            font_size: Font size for subtitles
            color: Text color in hex (default: white)
        """
        self.font_size = font_size
        self.color = color
    
    def generate_subtitles_srt(self, segments: List[Dict], output_path: str) -> bool:
        """
        Generate SRT format subtitles
        
        Args:
            segments: List of segments with text, start_time, end_time
            output_path: Path to save SRT file
        
        Returns:
            True if successful
        """
        try:
            srt_content = ""
            for idx, segment in enumerate(segments, 1):
                start = self._seconds_to_timestamp(segment['start_time'])
                end = self._seconds_to_timestamp(segment['end_time'])
                text = segment['text']
                
                srt_content += f"{idx}\n"
                srt_content += f"{start} --> {end}\n"
                srt_content += f"{text}\n\n"
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            return True
        except Exception as e:
            print(f"Failed to generate SRT: {str(e)}")
            return False
    
    def generate_subtitles_vtt(self, segments: List[Dict], output_path: str) -> bool:
        """
        Generate VTT format subtitles
        
        Args:
            segments: List of segments with text, start_time, end_time
            output_path: Path to save VTT file
        
        Returns:
            True if successful
        """
        try:
            vtt_content = "WEBVTT\n\n"
            
            for segment in segments:
                start = self._seconds_to_timestamp(segment['start_time'])
                end = self._seconds_to_timestamp(segment['end_time'])
                text = segment['text']
                
                vtt_content += f"{start} --> {end}\n"
                vtt_content += f"{text}\n\n"
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(vtt_content)
            
            return True
        except Exception as e:
            print(f"Failed to generate VTT: {str(e)}")
            return False
    
    def _seconds_to_timestamp(self, seconds: float) -> str:
        """
        Convert seconds to timestamp format (HH:MM:SS,mmm)
        
        Args:
            seconds: Time in seconds
        
        Returns:
            Formatted timestamp string
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((td.total_seconds() % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def embed_subtitles_in_video(self, video_path: str, subtitle_path: str, output_path: str) -> bool:
        """
        Embed subtitles into video using ffmpeg
        
        Args:
            video_path: Path to video file
            subtitle_path: Path to subtitle file
            output_path: Path to save video with embedded subtitles
        
        Returns:
            True if successful
        """
        import subprocess
        
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f"subtitles={subtitle_path}:force_style='FontSize={self.font_size}'",
                '-c:a', 'aac',
                '-c:v', 'libx264',
                '-preset', 'medium',
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except Exception as e:
            print(f"Failed to embed subtitles: {str(e)}")
            return False