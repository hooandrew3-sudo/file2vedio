# API Usage Examples

This document provides examples of how to use the File2Vedio API.

## Basic Setup

```bash
# Set API base URL
BASE_URL="http://localhost:5000"
```

## 1. Health Check

### cURL

```bash
curl -X GET "$BASE_URL/api/health"
```

### Python

```python
import requests

response = requests.get('http://localhost:5000/api/health')
print(response.json())
# Output: {'status': 'healthy'}
```

### JavaScript

```javascript
fetch('http://localhost:5000/api/health')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 2. Get Available Voices

### cURL

```bash
curl -X GET "$BASE_URL/api/voices"
```

### Python

```python
import requests

response = requests.get('http://localhost:5000/api/voices')
voices = response.json()['voices']
for lang, voice in voices.items():
    print(f"{lang}: {voice}")
```

## 3. Upload Article and Generate Video

### cURL

```bash
curl -X POST "$BASE_URL/api/upload" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Future of AI",
    "content": "Artificial Intelligence is transforming our world..."
  }'
```

### Python

```python
import requests
import json

data = {
    "title": "The Future of AI",
    "content": "Artificial Intelligence is transforming our world in ways we never imagined..."
}

response = requests.post(
    'http://localhost:5000/api/upload',
    json=data
)

result = response.json()
task_id = result['task_id']
print(f"Task ID: {task_id}")
print(f"Status: {result['status']}")
```

### JavaScript

```javascript
const data = {
  title: "The Future of AI",
  content: "Artificial Intelligence is transforming our world..."
};

fetch('http://localhost:5000/api/upload', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
  console.log('Task ID:', result.task_id);
  console.log('Status:', result.status);
});
```

## 4. Check Task Status

### cURL

```bash
# Replace TASK_ID with actual task ID
curl -X GET "$BASE_URL/api/status/TASK_ID"
```

### Python

```python
import requests
import time

task_id = "550e8400-e29b-41d4-a716-446655440000"

while True:
    response = requests.get(f'http://localhost:5000/api/status/{task_id}')
    status = response.json()
    
    print(f"Status: {status['status']}")
    print(f"Progress: {status['progress']}%")
    
    if status['status'] == 'completed':
        print("Video generation completed!")
        break
    elif status['status'] == 'failed':
        print(f"Error: {status['error']}")
        break
    
    time.sleep(2)  # Check every 2 seconds
```

### JavaScript

```javascript
const taskId = "550e8400-e29b-41d4-a716-446655440000";

const checkStatus = async () => {
  const response = await fetch(`http://localhost:5000/api/status/${taskId}`);
  const status = await response.json();
  
  console.log(`Status: ${status.status}`);
  console.log(`Progress: ${status.progress}%`);
  
  if (status.status === 'completed') {
    console.log('Video ready for download!');
  } else if (status.status === 'failed') {
    console.log(`Error: ${status.error}`);
  }
};

// Check every 2 seconds
setInterval(checkStatus, 2000);
```

## 5. Download Video

### cURL

```bash
curl -O "$BASE_URL/api/download/TASK_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Python

```python
import requests

task_id = "550e8400-e29b-41d4-a716-446655440000"

response = requests.get(
    f'http://localhost:5000/api/download/{task_id}',
    stream=True
)

# Save to file
with open('video.mp4', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

print("Video downloaded successfully!")
```

### JavaScript

```javascript
const downloadVideo = async (taskId) => {
  const response = await fetch(
    `http://localhost:5000/api/download/${taskId}`
  );
  
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'video.mp4';
  a.click();
  window.URL.revokeObjectURL(url);
};

downloadVideo("550e8400-e29b-41d4-a716-446655440000");
```

## Complete Workflow Example

### Python Complete Example

```python
import requests
import time
import json

class File2VedioClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
    
    def upload(self, title, content):
        """Upload article and start video generation"""
        data = {'title': title, 'content': content}
        response = requests.post(f'{self.base_url}/api/upload', json=data)
        return response.json()
    
    def get_status(self, task_id):
        """Get video generation status"""
        response = requests.get(f'{self.base_url}/api/status/{task_id}')
        return response.json()
    
    def wait_for_completion(self, task_id, timeout=600, poll_interval=2):
        """Wait for video to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_status(task_id)
            print(f"Status: {status['status']} | Progress: {status['progress']}%")
            
            if status['status'] == 'completed':
                return True
            elif status['status'] == 'failed':
                print(f"Error: {status['error']}")
                return False
            
            time.sleep(poll_interval)
        
        print("Timeout reached")
        return False
    
    def download_video(self, task_id, output_file='video.mp4'):
        """Download generated video"""
        response = requests.get(f'{self.base_url}/api/download/{task_id}', stream=True)
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Video saved to {output_file}")
    
    def generate_video(self, title, content, output_file='video.mp4'):
        """Complete workflow: upload -> wait -> download"""
        # Upload
        result = self.upload(title, content)
        task_id = result['task_id']
        print(f"Task started: {task_id}")
        
        # Wait for completion
        if self.wait_for_completion(task_id):
            # Download
            self.download_video(task_id, output_file)
            print(f"Success! Video saved to {output_file}")
        else:
            print("Failed to generate video")

# Usage
if __name__ == '__main__':
    client = File2VedioClient()
    
    title = "Introduction to Machine Learning"
    content = """
    Machine learning is a subset of artificial intelligence that enables 
    computers to learn from data without being explicitly programmed. 
    It has revolutionized many industries...
    """
    
    client.generate_video(title, content, 'output.mp4')
```

## Error Handling

### Python

```python
import requests
from requests.exceptions import RequestException

try:
    response = requests.post(
        'http://localhost:5000/api/upload',
        json={'title': 'Test', 'content': 'Content'},
        timeout=10
    )
    response.raise_for_status()  # Raise exception for bad status
    
except requests.exceptions.ConnectionError:
    print("Connection error: Server not reachable")
except requests.exceptions.Timeout:
    print("Request timeout")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except RequestException as e:
    print(f"Request error: {e}")
```

## Rate Limiting

Currently, the API does not have rate limiting enabled. For production deployments, consider implementing:

- Per-IP rate limiting
- Per-user rate limiting
- Queue-based processing

## Response Codes

- **200** - Success
- **202** - Accepted (async processing)
- **400** - Bad request
- **404** - Not found
- **500** - Server error

## More Examples

For more examples and use cases, check the `examples/` directory in the repository.
