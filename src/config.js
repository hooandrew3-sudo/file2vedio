/**
 * Configuration for Cloudflare deployment
 */

export const config = {
  // API endpoints
  api: {
    pythonBackend: process.env.PYTHON_BACKEND_URL || 'http://localhost:5000',
    timeout: 60000, // 60 seconds
  },

  // R2 bucket configuration
  r2: {
    bucketName: process.env.R2_BUCKET_NAME || 'file2vedio-videos',
    region: 'us-east-1',
  },

  // KV namespace configuration
  kv: {
    cacheTTL: 3600, // 1 hour
    rateLimitWindow: 60, // 1 minute
    rateLimitRequests: 100, // 100 requests per minute
  },

  // Security
  security: {
    corsOrigins: [
      'https://file2vedio.com',
      'https://www.file2vedio.com',
      'http://localhost:3000', // Development
    ],
    maxUploadSize: 52428800, // 50MB in bytes
  },

  // Feature flags
  features: {
    enableRateLimiting: true,
    enableCaching: true,
    enableVideoProcessing: true,
  },
};

// Environment-specific configuration
export const getConfig = (env) => {
  const baseConfig = { ...config };

  if (env === 'production') {
    baseConfig.security.corsOrigins = [
      'https://file2vedio.com',
      'https://www.file2vedio.com',
    ];
  } else if (env === 'staging') {
    baseConfig.api.pythonBackend = process.env.PYTHON_BACKEND_URL_STAGING;
  }

  return baseConfig;
};
