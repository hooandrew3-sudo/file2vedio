# File2Vedio - 文章转视频生成器

## 功能描述
从一篇文章（提炼）生成一段3分钟的视频，包含：
- 二次元画面
- 女生中速、有感情和停顿的配音
- 字幕
- MP4格式下载

## 项目结构
```
file2vedio/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── text_processor.py
│   │   ├── tts_engine.py
│   │   ├── video_generator.py
│   │   ├── subtitle_handler.py
│   │   └── anime_renderer.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── api.py
│   └── templates/
│       ├── index.html
│       └── download.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── uploads/
├── output_videos/
├── requirements.txt
├── .env.example
└── README.md
```

## 安装依赖
```bash
pip install -r requirements.txt
```

## 快速开始
```bash
python app/main.py
```

## 核心模块说明

### 1. text_processor.py
- 文章文本预处理
- 关键内容提取
- 段落分割和脚本生成

### 2. tts_engine.py
- 文本转语音（使用Edge TTS）
- 生成女性配音
- 音频处理和优化

### 3. video_generator.py
- 视频组合和编辑
- 配音和背景音乐混合
- MP4格式导出

### 4. subtitle_handler.py
- 字幕生成（SRT/VTT格式）
- 字幕时间同步
- 字幕样式配置

### 5. anime_renderer.py
- 二次元画面渲染
- 动画效果
- 场景切换

## API端点

### POST /api/upload
上传文章文本
```json
{
  "title": "文章标题",
  "content": "文章内容"
}
```

### GET /api/video/<video_id>
下载生成的视频

### GET /api/status/<task_id>
查询任务进度

## 许可证
MIT