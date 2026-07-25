/**
 * Cloudflare Worker for File2Vedio API Proxy
 * Handles requests and proxies to Python backend
 */

import { Router } from 'itty-router';

const router = Router();

// CORS middleware
const setCorsHeaders = (response) => {
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
  
  Object.keys(corsHeaders).forEach(key => {
    response.headers.set(key, corsHeaders[key]);
  });
  
  return response;
};

// Health check
router.get('/api/health', async () => {
  return setCorsHeaders(new Response(JSON.stringify({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: 'cloudflare-workers'
  }), {
    headers: { 'Content-Type': 'application/json' },
    status: 200
  }));
});

// Proxy to Python backend for video upload
router.post('/api/upload', async (request, env) => {
  try {
    const body = await request.json();
    
    // Validate input
    if (!body.title || !body.content) {
      return setCorsHeaders(new Response(JSON.stringify({
        error: 'Title and content are required'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      }));
    }
    
    // Forward to Python backend
    const backendUrl = env.PYTHON_BACKEND_URL || 'http://localhost:5000';
    const response = await fetch(`${backendUrl}/api/upload`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    
    const result = await response.json();
    
    return setCorsHeaders(new Response(JSON.stringify(result), {
      status: response.status,
      headers: { 'Content-Type': 'application/json' }
    }));
  } catch (error) {
    return setCorsHeaders(new Response(JSON.stringify({
      error: error.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    }));
  }
});

// Proxy status check
router.get('/api/status/:taskId', async (request, env) => {
  try {
    const { taskId } = request.params;
    const backendUrl = env.PYTHON_BACKEND_URL || 'http://localhost:5000';
    
    const response = await fetch(`${backendUrl}/api/status/${taskId}`);
    const result = await response.json();
    
    return setCorsHeaders(new Response(JSON.stringify(result), {
      status: response.status,
      headers: { 'Content-Type': 'application/json' }
    }));
  } catch (error) {
    return setCorsHeaders(new Response(JSON.stringify({
      error: error.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    }));
  }
});

// Proxy video download from R2
router.get('/api/download/:taskId', async (request, env) => {
  try {
    const { taskId } = request.params;
    
    // Get video from R2
    const videoKey = `videos/${taskId}.mp4`;
    const object = await env.VIDEOS.get(videoKey);
    
    if (!object) {
      return setCorsHeaders(new Response(JSON.stringify({
        error: 'Video not found'
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      }));
    }
    
    return setCorsHeaders(new Response(object.body, {
      status: 200,
      headers: {
        'Content-Type': 'video/mp4',
        'Content-Disposition': `attachment; filename="${taskId}.mp4"`
      }
    }));
  } catch (error) {
    return setCorsHeaders(new Response(JSON.stringify({
      error: error.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    }));
  }
});

// Get available voices
router.get('/api/voices', async (request, env) => {
  return setCorsHeaders(new Response(JSON.stringify({
    voices: {
      'zh-CN': 'zh-CN-XiaoxiaoNeural',
      'zh-TW': 'zh-TW-HsiaoChenNeural',
      'en-US': 'en-US-AriaNeural',
      'ja-JP': 'ja-JP-NanamiNeural',
      'ko-KR': 'ko-KR-SunHiNeural'
    }
  }), {
    headers: { 'Content-Type': 'application/json' },
    status: 200
  }));
});

// Handle 404
router.all('*', () => {
  return setCorsHeaders(new Response(JSON.stringify({
    error: 'Not Found'
  }), {
    status: 404,
    headers: { 'Content-Type': 'application/json' }
  }));
});

export default {
  fetch: router.handle
};
