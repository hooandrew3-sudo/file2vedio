/**
 * Cloudflare Worker for file2video
 * Handles edge requests and routes to backend
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    try {
      // Route handlers
      if (url.pathname === '/api/upload' && request.method === 'POST') {
        return handleUpload(request, env, corsHeaders);
      } else if (url.pathname.startsWith('/api/process') && request.method === 'POST') {
        return handleProcess(request, env, corsHeaders);
      } else if (url.pathname.startsWith('/api/status/')) {
        return handleStatus(request, env, corsHeaders);
      } else if (url.pathname.startsWith('/api/download/')) {
        return handleDownload(request, env, corsHeaders);
      } else if (url.pathname === '/health') {
        return new Response(JSON.stringify({ status: 'ok' }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }
      
      return new Response('Not found', { status: 404, headers: corsHeaders });
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};

async function handleUpload(request, env, corsHeaders) {
  const formData = await request.formData();
  const file = formData.get('file');
  
  if (!file) {
    return new Response(JSON.stringify({ error: 'No file provided' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
  
  const jobId = crypto.randomUUID();
  const buffer = await file.arrayBuffer();
  
  // Store in R2
  await env.UPLOAD_BUCKET.put(`${jobId}/${file.name}`, buffer, {
    httpMetadata: {
      contentType: file.type,
    },
    customMetadata: {
      originalName: file.name,
      uploadTime: new Date().toISOString()
    }
  });
  
  return new Response(JSON.stringify({
    success: true,
    jobId,
    message: 'File uploaded successfully',
    file: { originalName: file.name, size: file.size }
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

async function handleProcess(request, env, corsHeaders) {
  const { jobId, language = 'en' } = await request.json();
  
  if (!jobId) {
    return new Response(JSON.stringify({ error: 'jobId required' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
  
  // Queue processing job
  await env.PROCESSING_QUEUE.send({
    jobId,
    language,
    timestamp: new Date().toISOString()
  });
  
  return new Response(JSON.stringify({
    success: true,
    jobId,
    status: 'queued',
    message: 'Processing started'
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

async function handleStatus(request, env, corsHeaders) {
  const jobId = new URL(request.url).pathname.split('/').pop();
  
  // Get status from KV or database
  const status = await env.JOB_STATUS.get(jobId);
  
  return new Response(JSON.stringify(status || { error: 'Job not found' }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

async function handleDownload(request, env, corsHeaders) {
  const jobId = new URL(request.url).pathname.split('/').pop();
  
  // Get from R2
  const object = await env.VIDEO_BUCKET.get(`${jobId}.mp4`);
  
  if (!object) {
    return new Response(JSON.stringify({ error: 'Video not found' }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
  
  return new Response(object.body, {
    headers: {
      ...corsHeaders,
      'Content-Type': 'video/mp4',
      'Content-Disposition': `attachment; filename="${jobId}.mp4"`
    }
  });
}
