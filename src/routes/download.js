import fs from 'fs';
import path from 'path';
import { jobStore } from './upload.js';

export const downloadHandler = (req, res) => {
  try {
    const { jobId } = req.params;
    
    if (!jobId) {
      return res.status(400).json({ error: 'jobId is required' });
    }
    
    const job = jobStore.get(jobId);
    
    if (!job) {
      return res.status(404).json({ error: 'Job not found' });
    }
    
    if (job.status !== 'completed') {
      return res.status(400).json({ 
        error: 'Video is not ready',
        status: job.status,
        progress: job.progress
      });
    }
    
    const videoPath = job.videoPath;
    
    if (!fs.existsSync(videoPath)) {
      return res.status(404).json({ error: 'Video file not found' });
    }
    
    const fileSize = fs.statSync(videoPath).size;
    
    res.setHeader('Content-Type', 'video/mp4');
    res.setHeader('Content-Length', fileSize);
    res.setHeader('Content-Disposition', `attachment; filename="${jobId}.mp4"`);
    
    const stream = fs.createReadStream(videoPath);
    stream.pipe(res);
    
    stream.on('error', (error) => {
      console.error('Download error:', error);
      res.status(500).json({ error: 'Error downloading file' });
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
