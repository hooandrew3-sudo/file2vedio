# File2Vedio - 文章转视频生成器

## 快速开始

### 1. 环境准备

#### 系统依赖
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 下载并安装: https://ffmpeg.org/download.html
```

#### Python依赖
```bash
pip install -r requirements.txt
```

### 2. 配置

```bash
cp .env.example .env
```

编辑 `.env` 文件配置参数：
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
TTS_VOICE=zh-CN-XiaoxiaoNeural  # 女性中文配音
TTS_RATE=0.9  # 语速（推荐0.8-1.2）
```

### 3. 运行应用

```bash
python app/main.py
```

访问: http://localhost:5000

## 功能模块说明

### TextProcessor (文本处理)
- 自动提取关键内容
- 将长文章压缩到3分钟
- 按段落分割文本用于字幕
- 估算朗读时长

### TTSEngine (文本转语音)
- 使用微软Edge TTS
- 支持多种女性配音
- 可调整语速
- 支持多语言

### VideoGenerator (视频生成)
- 组合音频和背景图像
- 支持多张图片序列
- FFmpeg后端
- MP4格式输出

### SubtitleHandler (字幕处理)
- 生成SRT格式字幕
- 自动时间同步
- 支持嵌入视频
- 可自定义样式

### AnimeRenderer (二次元渲染)
- 生成动漫风格背景
- 多种配色方案
- 添加文本叠加
- 帧序列生成

## API文档

### 1. 上传文章并开始生成

**POST** `/api/upload`

请求体：
```json
{
  "title": "文章标题",
  "content": "文章内容"
}
```

响应：
```json
{
  "task_id": "uuid-string",
  "status": "processing"
}
```

### 2. 查询任务状态

**GET** `/api/status/<task_id>`

响应：
```json
{
  "status": "processing|completed|failed",
  "progress": 0-100,
  "title": "文章标题",
  "error": null
}
```

### 3. 下载视频

**GET** `/api/download/<task_id>`

返回MP4文件

### 4. 获取可用配音

**GET** `/api/voices`

响应：
```json
{
  "voices": {
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "zh-TW": "zh-TW-HsiaoChenNeural",
    ...
  }
}
```

## 项目架构

```
file2vedio/
├── app/
│   ├── __init__.py              # Flask应用工厂
│   ├── main.py                  # 应用入口
│   ├── config.py                # 配置文件
│   ├── modules/
│   │   ├── text_processor.py    # 文本处理
│   │   ├── tts_engine.py        # 语音合成
│   │   ├── subtitle_handler.py  # 字幕处理
│   │   ├── video_generator.py   # 视频生成
│   │   └── anime_renderer.py    # 动漫渲染
│   ├── routes/
│   │   └── api.py               # API路由
│   ├── templates/
│   │   └── index.html           # Web界面
│   └── static/
│       ├── css/style.css        # 样式
│       └── js/app.js            # 前端逻辑
├── uploads/                     # 上传文件目录
├── output_videos/               # 输出视频目录
├── requirements.txt             # Python依赖
└── .env.example                 # 环境变量示例
```

## 处理流程

1. **文本处理** → 提取核心内容，适配3分钟时长
2. **语音合成** → 将文本转换为女性配音
3. **字幕生成** → 创建时间同步的字幕文件
4. **背景渲染** → 生成二次元风格背景
5. **视频合成** → 组合音频、背景、字幕
6. **输出下载** → MP4格式提供下载

## 性能优化建议

### 生产环境部署

1. 使用**Celery**进行异步任务处理
2. 使用**Redis**缓存和任务队列
3. 部署**Gunicorn** WSGI服务器
4. 配置**Nginx**反向代理

### 资源优化

- 视频分辨率调整：修改`VIDEO_WIDTH`和`VIDEO_HEIGHT`
- FFmpeg编码优化：调整`VIDEO_BITRATE`
- 并发处理：增加worker数量

## 故障排查

### FFmpeg未找到
```bash
# Linux
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### TTS失败
- 检查网络连接
- 尝试更换voice参数
- 查看日志输出

### 视频生成缓慢
- 降低视频分辨率
- 减少FFmpeg编码时间
- 使用GPU加速（如果可用）

## 开发路线图

- [ ] Web UI优化
- [ ] 支持上传图片作为背景
- [ ] 更多动画效果
- [ ] 背景音乐添加
- [ ] 自定义字幕样式
- [ ] 批量处理
- [ ] 视频模板库
- [ ] 数据库集成

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 支持

如有问题，请提交Issue或联系维护者。