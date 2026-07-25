#!/bin/bash
# Installation and setup script for File2Vedio

set -e

echo "🎬 File2Vedio - Installation Script"
echo "====================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $PYTHON_VERSION"

if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "⚠️  FFmpeg not found. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install -y ffmpeg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg
    else
        echo "❌ Please install FFmpeg manually: https://ffmpeg.org/download.html"
        exit 1
    fi
else
    echo "✓ FFmpeg is installed"
    ffmpeg -version | head -1
fi

echo ""
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "⚙️  Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo "  📝 Please edit .env to customize settings"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 To start the server, run:"
echo "   python app/main.py"
echo ""
echo "🌐 Then open your browser to:"
echo "   http://localhost:5000"
echo ""
