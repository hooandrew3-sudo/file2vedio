class FileToVideoApp {
    constructor() {
        this.taskId = null;
        this.statusCheckInterval = null;
        this.initEventListeners();
    }

    initEventListeners() {
        document.getElementById('uploadForm').addEventListener('submit', (e) => this.handleUpload(e));
        document.getElementById('downloadBtn').addEventListener('click', () => this.downloadVideo());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetForm());
        document.getElementById('retryBtn').addEventListener('click', () => this.resetForm());
    }

    async handleUpload(e) {
        e.preventDefault();

        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;
        const voice = document.getElementById('voice').value;

        if (!title || !content) {
            alert('请输入标题和内容');
            return;
        }

        // Hide form, show status
        this.hideAllSections();
        document.getElementById('statusSection').style.display = 'block';

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, content, voice })
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const data = await response.json();
            this.taskId = data.task_id;

            // Start checking status
            this.startStatusCheck();
        } catch (error) {
            this.showError('上传失败: ' + error.message);
        }
    }

    startStatusCheck() {
        this.statusCheckInterval = setInterval(() => this.checkStatus(), 2000);
    }

    async checkStatus() {
        try {
            const response = await fetch(`/api/status/${this.taskId}`);
            const data = await response.json();

            const progress = data.progress || 0;
            document.getElementById('progressFill').style.width = progress + '%';
            document.getElementById('progressText').textContent = `处理中... ${progress}%`;

            if (data.status === 'completed') {
                clearInterval(this.statusCheckInterval);
                this.showResult(data);
            } else if (data.status === 'failed') {
                clearInterval(this.statusCheckInterval);
                this.showError('视频生成失败: ' + (data.error || '未知错误'));
            }
        } catch (error) {
            console.error('Status check error:', error);
        }
    }

    showResult(data) {
        this.hideAllSections();
        document.getElementById('resultSection').style.display = 'block';
    }

    showError(message) {
        this.hideAllSections();
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('errorSection').style.display = 'block';
    }

    downloadVideo() {
        const downloadUrl = `/api/download/${this.taskId}`;
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = 'video.mp4';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    resetForm() {
        document.getElementById('uploadForm').reset();
        this.hideAllSections();
        document.querySelector('.upload-section').style.display = 'block';
        this.taskId = null;
    }

    hideAllSections() {
        document.getElementById('uploadForm').parentElement.style.display = 'none';
        document.getElementById('statusSection').style.display = 'none';
        document.getElementById('resultSection').style.display = 'none';
        document.getElementById('errorSection').style.display = 'none';
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new FileToVideoApp();
});
