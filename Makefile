# Makefile for File2Vedio

.PHONY: install run dev clean test help

help:
	@echo "File2Vedio - Makefile Commands"
	@echo "==============================="
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run production server"
	@echo "  make dev        - Run development server"
	@echo "  make clean      - Clean up temp files"
	@echo "  make test       - Run tests"
	@echo "  make format     - Format code with black"
	@echo "  make lint       - Lint code with flake8"

.DEFAULT_GOAL := help

install:
	@echo "📦 Installing dependencies..."
	@pip install --upgrade pip
	@pip install -r requirements.txt
	@echo "✓ Dependencies installed"

run:
	@echo "🚀 Starting production server..."
	@python app/main.py

dev:
	@echo "🔧 Starting development server..."
	@FLASK_DEBUG=True python app/main.py

clean:
	@echo "🧹 Cleaning up..."
	@rm -rf __pycache__ .pytest_cache *.pyc
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@rm -rf temp/* output_videos/*
	@echo "✓ Cleaned up"

test:
	@echo "🧪 Running tests..."
	@pytest -v

format:
	@echo "📐 Formatting code..."
	@black app/
	@echo "✓ Code formatted"

lint:
	@echo "🔍 Linting code..."
	@flake8 app/ --max-line-length=120

setup-env:
	@if [ ! -f .env ]; then cp .env.example .env; echo "✓ Created .env file"; else echo "✓ .env already exists"; fi

setup: install setup-env
	@echo "✓ Setup complete! Run 'make dev' to start."
