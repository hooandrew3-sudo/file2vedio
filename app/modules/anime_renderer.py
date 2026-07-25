import os
import logging
from typing import List, Tuple
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

class AnimeRenderer:
    """
    Render anime/2D style video frames
    """
    
    def __init__(self, width: int = 1280, height: int = 720):
        """
        Initialize anime renderer
        
        Args:
            width: Frame width
            height: Frame height
        """
        self.width = width
        self.height = height
    
    def create_anime_background(self, output_path: str, color_scheme: str = 'default') -> bool:
        """
        Create a simple anime-style background
        
        Args:
            output_path: Path to save background image
            color_scheme: Color scheme ('default', 'warm', 'cool', 'dark')
        
        Returns:
            True if successful
        """
        try:
            # Define color schemes (BGR for OpenCV)
            schemes = {
                'default': {'main': (255, 200, 100), 'accent': (100, 150, 200)},
                'warm': {'main': (100, 150, 200), 'accent': (200, 100, 50)},
                'cool': {'main': (200, 100, 150), 'accent': (100, 200, 200)},
                'dark': {'main': (50, 50, 80), 'accent': (100, 100, 150)}
            }
            
            colors = schemes.get(color_scheme, schemes['default'])
            
            # Create gradient background
            img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Create gradient from top to bottom
            for i in range(self.height):
                alpha = i / self.height
                color = (
                    int(colors['main'][0] * (1 - alpha) + colors['accent'][0] * alpha),
                    int(colors['main'][1] * (1 - alpha) + colors['accent'][1] * alpha),
                    int(colors['main'][2] * (1 - alpha) + colors['accent'][2] * alpha)
                )
                img[i, :] = color
            
            # Add some decorative elements
            self._add_anime_elements(img)
            
            # Save image
            cv2.imwrite(output_path, img)
            logger.info(f"Anime background created: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to create anime background: {str(e)}")
            return False
    
    def _add_anime_elements(self, img: np.ndarray) -> None:
        """
        Add decorative anime elements to image
        
        Args:
            img: Image array to modify
        """
        height, width = img.shape[:2]
        
        # Add subtle circles/bubbles
        centers = [
            (int(width * 0.2), int(height * 0.3)),
            (int(width * 0.8), int(height * 0.7)),
            (int(width * 0.5), int(height * 0.2))
        ]
        
        for center in centers:
            cv2.circle(img, center, 50, (200, 200, 200), -1)
            cv2.circle(img, center, 50, (150, 150, 150), 2)
    
    def add_text_to_image(
        self,
        image_path: str,
        text: str,
        output_path: str,
        position: Tuple[int, int] = None,
        font_size: int = 40,
        color: Tuple[int, int, int] = (255, 255, 255)
    ) -> bool:
        """
        Add text overlay to image
        
        Args:
            image_path: Path to image
            text: Text to add
            output_path: Path to save modified image
            position: Position (x, y) for text
            font_size: Font size
            color: Text color in RGB
        
        Returns:
            True if successful
        """
        try:
            img = Image.open(image_path).convert('RGB')
            draw = ImageDraw.Draw(img)
            
            # Default position: center
            if position is None:
                position = (self.width // 2, self.height // 2)
            
            # Try to use default font, fallback to PIL default
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Add text with outline effect
            outline_color = (0, 0, 0)
            outline_width = 2
            
            for adj_x in range(-outline_width, outline_width + 1):
                for adj_y in range(-outline_width, outline_width + 1):
                    if adj_x != 0 or adj_y != 0:
                        draw.text((position[0] + adj_x, position[1] + adj_y), text, font=font, fill=outline_color)
            
            # Draw main text
            draw.text(position, text, font=font, fill=color)
            
            img.save(output_path)
            logger.info(f"Text added to image: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to add text to image: {str(e)}")
            return False
    
    def create_frame_sequence(
        self,
        duration_seconds: float,
        fps: int,
        output_dir: str,
        background_color: Tuple[int, int, int] = (100, 150, 200)
    ) -> bool:
        """
        Create a sequence of anime frames
        
        Args:
            duration_seconds: Duration of sequence
            fps: Frames per second
            output_dir: Directory to save frames
            background_color: RGB background color
        
        Returns:
            True if successful
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            frame_count = int(duration_seconds * fps)
            
            for i in range(frame_count):
                # Create frame
                frame = np.ones((self.height, self.width, 3), dtype=np.uint8)
                frame[:] = background_color
                
                # Add simple animation
                progress = i / frame_count
                circle_y = int(self.height * (0.3 + 0.4 * np.sin(progress * 2 * np.pi)))
                cv2.circle(frame, (self.width // 2, circle_y), 50, (255, 255, 255), -1)
                
                # Save frame
                frame_path = os.path.join(output_dir, f"frame_{i:06d}.png")
                cv2.imwrite(frame_path, frame)
            
            logger.info(f"Frame sequence created: {frame_count} frames in {output_dir}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to create frame sequence: {str(e)}")
            return False