#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for File2Vedio modules
"""

import unittest
import os
import tempfile
from app.modules.text_processor import TextProcessor
from app.modules.tts_engine import TTSEngine
from app.modules.subtitle_handler import SubtitleHandler
from app.modules.anime_renderer import AnimeRenderer


class TestTextProcessor(unittest.TestCase):
    """Test TextProcessor module"""
    
    def setUp(self):
        self.processor = TextProcessor(max_duration=180)
    
    def test_clean_text(self):
        """Test text cleaning"""
        text = "这是一个测试句子。http://example.com  多余空格"
        cleaned = self.processor._clean_text(text)
        self.assertNotIn('http', cleaned)
        self.assertNotIn('  ', cleaned)
    
    def test_split_sentences(self):
        """Test sentence splitting"""
        text = "这是第一句。这是第二句。这是第三句。"
        sentences = self.processor._split_sentences(text)
        self.assertEqual(len(sentences), 3)
    
    def test_estimate_duration(self):
        """Test duration estimation"""
        text = "这是测试文本。" * 10
        duration = self.processor.estimate_duration(text)
        self.assertGreater(duration, 0)
    
    def test_extract_key_content(self):
        """Test key content extraction"""
        text = "这是第一句。" * 50
        extracted = self.processor.extract_key_content(text, target_words=20)
        self.assertIsNotNone(extracted)
        self.assertGreater(len(extracted), 0)


class TestSubtitleHandler(unittest.TestCase):
    """Test SubtitleHandler module"""
    
    def setUp(self):
        self.handler = SubtitleHandler(font_size=32, color='ffffff')
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Clean up temp files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_seconds_to_timestamp(self):
        """Test timestamp conversion"""
        timestamp = self.handler._seconds_to_timestamp(65.5)
        self.assertEqual(timestamp, "00:01:05,500")
    
    def test_generate_srt(self):
        """Test SRT subtitle generation"""
        segments = [
            {'text': 'First subtitle', 'start_time': 0, 'end_time': 2},
            {'text': 'Second subtitle', 'start_time': 2, 'end_time': 4}
        ]
        output_path = os.path.join(self.temp_dir, 'test.srt')
        result = self.handler.generate_subtitles_srt(segments, output_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
    
    def test_generate_vtt(self):
        """Test VTT subtitle generation"""
        segments = [
            {'text': 'First subtitle', 'start_time': 0, 'end_time': 2},
            {'text': 'Second subtitle', 'start_time': 2, 'end_time': 4}
        ]
        output_path = os.path.join(self.temp_dir, 'test.vtt')
        result = self.handler.generate_subtitles_vtt(segments, output_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))


class TestTTSEngine(unittest.TestCase):
    """Test TTSEngine module"""
    
    def setUp(self):
        self.engine = TTSEngine(voice='zh-CN-XiaoxiaoNeural', rate=0.9)
    
    def test_validate_rate(self):
        """Test rate validation"""
        self.assertEqual(TTSEngine._validate_rate(0.5), 0.5)
        self.assertEqual(TTSEngine._validate_rate(2.0), 2.0)
        self.assertEqual(TTSEngine._validate_rate(0.1), 0.5)  # Clamped
        self.assertEqual(TTSEngine._validate_rate(2.5), 2.0)  # Clamped
    
    def test_available_voices(self):
        """Test available voices"""
        voices = TTSEngine.get_available_voices()
        self.assertIsNotNone(voices)
        self.assertIn('zh-CN', voices)
        self.assertIn('en-US', voices)
    
    def test_set_voice(self):
        """Test setting voice by language"""
        self.engine.set_voice('en-US')
        self.assertEqual(self.engine.voice, 'en-US-AriaNeural')


class TestAnimeRenderer(unittest.TestCase):
    """Test AnimeRenderer module"""
    
    def setUp(self):
        self.renderer = AnimeRenderer(width=1280, height=720)
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Clean up temp files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_create_background(self):
        """Test anime background creation"""
        output_path = os.path.join(self.temp_dir, 'background.png')
        result = self.renderer.create_anime_background(output_path, color_scheme='cool')
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))


class TestFlaskApp(unittest.TestCase):
    """Test Flask application"""
    
    def setUp(self):
        from app import create_app
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
    
    def test_voices_endpoint(self):
        """Test voices endpoint"""
        response = self.client.get('/api/voices')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('voices', data)
    
    def test_upload_missing_content(self):
        """Test upload with missing content"""
        response = self.client.post('/api/upload',
                                   json={'title': 'Test'})
        self.assertEqual(response.status_code, 400)
    
    def test_upload_valid_content(self):
        """Test upload with valid content"""
        response = self.client.post('/api/upload',
                                   json={
                                       'title': 'Test Article',
                                       'content': 'This is test content.' * 50
                                   })
        self.assertEqual(response.status_code, 202)
        data = response.get_json()
        self.assertIn('task_id', data)
        self.assertEqual(data['status'], 'processing')


if __name__ == '__main__':
    unittest.main()