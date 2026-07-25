import re
from typing import List, Dict, Tuple
import os

class TextProcessor:
    """
    Process and prepare text for video generation
    """
    
    def __init__(self, max_duration: int = 180):
        """
        Args:
            max_duration: Maximum video duration in seconds
        """
        self.max_duration = max_duration
        self.words_per_second = 4  # Average speech rate
    
    def extract_key_content(self, text: str, target_words: int = None) -> str:
        """
        Extract key content from article text
        
        Args:
            text: Full article text
            target_words: Target word count (default based on max_duration)
        
        Returns:
            Processed text with key content
        """
        if target_words is None:
            target_words = int(self.max_duration * self.words_per_second)
        
        # Clean text
        text = self._clean_text(text)
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        # Select important sentences
        selected = self._select_important_sentences(sentences, target_words)
        
        return ' '.join(selected)
    
    def split_into_segments(self, text: str, max_chars_per_segment: int = 100) -> List[str]:
        """
        Split text into segments for subtitle display
        
        Args:
            text: Text to split
            max_chars_per_segment: Maximum characters per segment
        
        Returns:
            List of text segments
        """
        sentences = self._split_sentences(text)
        segments = []
        current_segment = ""
        
        for sentence in sentences:
            if len(current_segment) + len(sentence) <= max_chars_per_segment:
                current_segment += sentence + " "
            else:
                if current_segment:
                    segments.append(current_segment.strip())
                current_segment = sentence + " "
        
        if current_segment:
            segments.append(current_segment.strip())
        
        return segments
    
    def estimate_duration(self, text: str) -> float:
        """
        Estimate speech duration in seconds
        
        Args:
            text: Text to analyze
        
        Returns:
            Estimated duration in seconds
        """
        # Count Chinese characters and English words
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        
        # Chinese: ~2 characters per second, English: ~4 words per second
        duration = (chinese_chars / 2) + (english_words / 4)
        return duration
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        """
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep Chinese and English
        text = re.sub(r'[^\w\s\u4e00-\u9fff\.\,\!\?\。\，\！\？]', '', text)
        
        return text
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        """
        # Split by common sentence endings
        sentences = re.split(r'[。\!！？？\.]', text)
        
        # Filter out empty sentences and strip whitespace
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _select_important_sentences(self, sentences: List[str], target_words: int) -> List[str]:
        """
        Select important sentences based on word count
        """
        selected = []
        word_count = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            if word_count + sentence_words <= target_words:
                selected.append(sentence)
                word_count += sentence_words
            elif word_count < target_words:
                # Add partial sentence if space remains
                selected.append(sentence)
                break
        
        return selected if selected else sentences[:5]  # Fallback to first 5 sentences
    
    def generate_script(self, text: str) -> Dict[str, any]:
        """
        Generate script with timing information
        
        Args:
            text: Text to convert to script
        
        Returns:
            Dictionary with script segments and timing
        """
        segments = self.split_into_segments(text)
        script = []
        current_time = 0
        
        for segment in segments:
            duration = self.estimate_duration(segment)
            script.append({
                'text': segment,
                'start_time': current_time,
                'end_time': current_time + duration,
                'duration': duration
            })
            current_time += duration
        
        return {
            'total_duration': current_time,
            'segments': script
        }