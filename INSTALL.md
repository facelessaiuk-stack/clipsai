# 🚀 Installation Guide - Faceless Video AI

This guide provides comprehensive instructions for installing and setting up the Faceless Video AI system on various platforms.

## 📋 Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+), macOS 10.15+, Windows 10+
- **Python**: 3.9 or higher
- **RAM**: Minimum 8GB, Recommended 16GB+
- **Storage**: Minimum 10GB free space
- **GPU**: Optional but recommended (NVIDIA with CUDA support)

### Required System Dependencies

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    ffmpeg \
    libmagic1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgtk-3-0

# Install CUDA dependencies (if using NVIDIA GPU)
sudo apt install -y nvidia-cuda-toolkit
```

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install \
    python@3.9 \
    ffmpeg \
    libmagic \
    cuda

# Install Xcode command line tools
xcode-select --install
```

#### Windows
```bash
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install system dependencies
choco install \
    python \
    ffmpeg \
    cuda \
    visualstudio2019buildtools
```

## 🐍 Python Environment Setup

### 1. Create Virtual Environment

```bash
# Navigate to project directory
cd faceless-video-ai

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Upgrade pip and setuptools

```bash
pip install --upgrade pip setuptools wheel
```

## 📦 Installation Methods

### Method 1: Install from Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/facelessvideoai/faceless-video-ai.git
cd faceless-video-ai

# Install in development mode
pip install -e .
```

### Method 2: Install from PyPI

```bash
# Install basic version
pip install faceless-video-ai

# Install with all optional dependencies
pip install faceless-video-ai[full]

# Install with development dependencies
pip install faceless-video-ai[dev]
```

### Method 3: Install with GPU Support

```bash
# Install with GPU acceleration
pip install faceless-video-ai[gpu]

# Install with all features including GPU
pip install faceless-video-ai[full,gpu]
```

## 🔧 Component-Specific Installation

### Text-to-Speech Engines

#### WhisperSpeech
```bash
# Install WhisperSpeech
pip install whisperspeech

# Download models (optional, will be downloaded automatically)
python -c "import whisperspeech; whisperspeech.load_model('librelight')"
```

#### Piper TTS
```bash
# Install Piper
pip install piper-tts

# Download voice models
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US-amy-low.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US-amy-low.onnx.json
```

#### XTTS
```bash
# Install TTS library
pip install TTS

# Download XTTS model
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

### Video Composition Engines

#### libopenshot
```bash
# Install libopenshot
pip install openshot-qt libopenshot

# On Ubuntu, you might also need:
sudo apt install -y openshot-qt
```

#### MoviePy
```bash
# Install MoviePy
pip install moviepy

# Install additional codecs
pip install imageio-ffmpeg
```

### AI Models

#### Stable Diffusion
```bash
# Install diffusers
pip install diffusers transformers accelerate

# Download model
python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
```

#### OpenAI Integration
```bash
# Install OpenAI client
pip install openai

# Set API key
export OPENAI_API_KEY="your_api_key_here"
```

## ⚙️ Configuration Setup

### 1. Environment Variables

Create a `.env` file in your project directory:

```bash
# TTS Configuration
TTS_ENGINE=whisperspeech
TTS_QUALITY=high
TTS_LANGUAGE=en

# Video Configuration
VIDEO_RESOLUTION=1920x1080
VIDEO_FPS=30
USE_GPU=true

# API Keys (optional)
OPENAI_API_KEY=your_openai_key_here
UNSPLASH_API_KEY=your_unsplash_key_here
PEXELS_API_KEY=your_pexels_key_here

# System Configuration
MAX_CONCURRENT_JOBS=4
LOG_LEVEL=INFO
```

### 2. Configuration File

Create `config.yaml`:

```yaml
tts:
  engine: whisperspeech
  quality: high
  language: en
  whisperspeech_model: librelight
  whisperspeech_device: auto

video:
  resolution: [1920, 1080]
  fps: 30
  codec: libx264
  use_libopenshot: true
  use_moviepy_fallback: true
  image_style: modern
  transition_duration: 0.5

content:
  model: gpt-3.5-turbo
  max_tokens: 2000
  temperature: 0.7
  default_style: educational
  include_subtitles: true

system:
  temp_dir: /tmp/faceless_video_ai
  output_dir: ./generated_videos
  max_concurrent_jobs: 4
  log_level: INFO
  use_gpu: true
  max_memory_gb: 8
  enable_cache: true
```

## 🧪 Testing the Installation

### 1. Basic Test

```bash
# Test basic functionality
python -c "from faceless_video_ai import FacelessVideoAI; print('✅ Import successful!')"
```

### 2. System Status Check

```bash
# Check system status
python cli.py status
```

### 3. Run Demo

```bash
# Run comprehensive demo
python examples/demo.py
```

### 4. Quick Video Generation

```bash
# Generate a test video
python cli.py generate --topic "Test Video" --duration 30 --style educational
```

## 🚨 Troubleshooting

### Common Issues

#### Import Errors
```bash
# If you get import errors, ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall the package
pip install -e .
```

#### FFmpeg Issues
```bash
# Check if FFmpeg is installed
ffmpeg -version

# If not found, install it
# Ubuntu/Debian:
sudo apt install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
choco install ffmpeg
```

#### CUDA Issues
```bash
# Check CUDA installation
nvidia-smi

# Check PyTorch CUDA support
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Reinstall PyTorch with CUDA support
pip uninstall torch torchaudio
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### Memory Issues
```bash
# Reduce batch size and concurrent jobs
export MAX_CONCURRENT_JOBS=2

# Use lower resolution
export VIDEO_RESOLUTION=1280x720

# Enable memory optimization
export ENABLE_MEMORY_OPTIMIZATION=true
```

### Performance Optimization

#### GPU Acceleration
```bash
# Ensure CUDA is properly installed
nvidia-smi

# Install PyTorch with CUDA support
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Set environment variables
export CUDA_VISIBLE_DEVICES=0
export USE_GPU=true
```

#### Memory Management
```bash
# Optimize memory usage
export MAX_MEMORY_GB=4
export ENABLE_MEMORY_OPTIMIZATION=true
export BATCH_SIZE=1
```

## 🔄 Updating

### Update from Source
```bash
# Pull latest changes
git pull origin main

# Reinstall package
pip install -e . --upgrade
```

### Update Dependencies
```bash
# Update all dependencies
pip install -r requirements.txt --upgrade

# Update specific components
pip install --upgrade whisperspeech piper-tts TTS
```

## 📚 Next Steps

After successful installation:

1. **Read the Documentation**: Check out the [README.md](README.md) for usage examples
2. **Run the Demo**: Execute `python examples/demo.py` to see all features
3. **Try the CLI**: Use `python cli.py --help` to explore command-line options
4. **Customize Configuration**: Modify `config.yaml` to suit your needs
5. **Join the Community**: Visit our [GitHub Discussions](https://github.com/facelessvideoai/faceless-video-ai/discussions)

## 🆘 Getting Help

If you encounter issues:

1. **Check the Troubleshooting section** above
2. **Search existing issues** on [GitHub Issues](https://github.com/facelessvideoai/faceless-video-ai/issues)
3. **Create a new issue** with detailed error information
4. **Join our community** on [GitHub Discussions](https://github.com/facelessvideoai/faceless-video-ai/discussions)

---

**Happy video creating! 🎬✨**