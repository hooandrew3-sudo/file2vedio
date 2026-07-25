import asyncio
import os
import edge_tts
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class TTSEngine:
    """
    Text-to-Speech engine using Microsoft Edge TTS
    """
    
    # Available female voices
    FEMALE_VOICES = {
        'zh-CN': 'zh-CN-XiaoxiaoNeural',  # Female, young
        'zh-TW': 'zh-TW-HsiaoChenNeural',  # Female
        'en-US': 'en-US-AriaNeural',       # Female
        'ja-JP': 'ja-JP-NanamiNeural',     # Female
        'ko-KR': 'ko-KR-SunHiNeural'       # Female
    }
    
    def __init__(self, voice: str = 'zh-CN-XiaoxiaoNeural', rate: float = 0.9):
        """
        Initialize TTS engine
        
        Args:
            voice: Voice name (default: Chinese female voice)
            rate: Speech rate (0.5 - 2.0, default: 0.9 for natural speed)
        """
        self.voice = voice
        self.rate = self._validate_rate(rate)
    
    async def synthesize_async(self, text: str, output_path: str) -> bool:
        """
        Asynchronously synthesize text to speech
        
        Args:
            text: Text to synthesize
            output_path: Path to save audio file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create TTS object
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.voice,
                rate=self.rate
            )
            
            # Save to file
            await communicate.save(output_path)
            logger.info(f"Audio synthesized successfully: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"TTS synthesis failed: {str(e)}")
            return False
    
    def synthesize(self, text: str, output_path: str) -> bool:
        """
        Synchronous wrapper for synthesize_async
        
        Args:
            text: Text to synthesize
            output_path: Path to save audio file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.synthesize_async(text, output_path))
    
    def set_voice(self, language: str) -> None:
        """
        Set voice based on language
        
        Args:
            language: Language code (e.g., 'zh-CN', 'en-US')
        """
        if language in self.FEMALE_VOICES:
            self.voice = self.FEMALE_VOICES[language]
        else:
            logger.warning(f"Language {language} not supported, using default")
    
    def set_rate(self, rate: float) -> None:
        """
        Set speech rate
        
        Args:
            rate: Rate value (0.5 - 2.0)
        """
        self.rate = self._validate_rate(rate)
    
    @staticmethod
    def _validate_rate(rate: float) -> float:
        """
        Validate and clamp speech rate
        
        Args:
            rate: Rate value
        
        Returns:
            Validated rate value
        """
        return max(0.5, min(2.0, rate))
    
    @staticmethod
    def get_available_voices() -> dict:
        """
        Get all available female voices
        
        Returns:
            Dictionary of available voices
        """
        return TTSEngine.FEMALE_VOICES