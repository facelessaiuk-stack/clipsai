# 🎬 Faceless Video AI

**Market-Leading Open-Source Faceless Video Software**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/faceless-video-ai.svg)](https://badge.fury.io/py/faceless-video-ai)

A comprehensive, open-source solution for automated faceless video creation that integrates advanced artificial intelligence for content generation, high-fidelity audio-visual output, and a modular architecture designed for exceptional scalability and customization.

## 🚀 Features

### ✨ AI-Powered Content Generation
- **Automated Script Writing**: Generate engaging video scripts from topics using AI models
- **Content Intelligence**: Smart content structuring with key points and visual elements
- **Multi-Style Support**: Educational, entertainment, news, and custom content styles
- **Audience Targeting**: Tailored content for specific demographics and use cases

### 🎤 High-Quality Text-to-Speech
- **WhisperSpeech Integration**: State-of-the-art TTS with 12x real-time generation
- **Piper TTS**: Fast, local neural TTS system for low-latency applications
- **XTTS Support**: Industrial-level controllable TTS with voice cloning
- **Multi-Language**: Support for multiple languages and accents
- **Voice Customization**: Adjustable speed, pitch, and clarity settings

### 🎬 Professional Video Composition
- **libopenshot Engine**: Award-winning video editor with Python bindings
- **MoviePy Fallback**: Robust Python video editing library
- **Advanced Effects**: Multi-layer compositing, transitions, and visual effects
- **Hardware Acceleration**: GPU-accelerated rendering for faster processing
- **Multi-Format Support**: Export to various video formats and resolutions

### 🖼️ AI-Generated Visual Assets
- **Stable Diffusion**: High-quality image generation from text descriptions
- **Dynamic Content**: Automatically generated visuals based on script content
- **Style Consistency**: Maintained visual coherence throughout videos
- **Placeholder System**: Fallback images when AI generation is unavailable

### 🔧 Modular Architecture
- **Plugin System**: Easy integration of new TTS engines and video processors
- **Configuration Management**: Flexible settings for all components
- **Resource Optimization**: Efficient memory and GPU usage management
- **Batch Processing**: Generate multiple videos simultaneously

## 🛠️ Installation

### Prerequisites

- **Python 3.9+**
- **FFmpeg** (for video processing)
- **CUDA-compatible GPU** (optional, for acceleration)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/facelessvideoai/faceless-video-ai.git
cd faceless-video-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Alternative: PyPI Install

```bash
pip install faceless-video-ai[full]
```

## 🚀 Quick Start

### Basic Usage

```python
import asyncio
from faceless_video_ai import FacelessVideoAI

async def main():
    # Initialize the system
    fvai = FacelessVideoAI()
    
    # Generate a video from a topic
    video_path = await fvai.generate_video_from_topic(
        topic="Artificial Intelligence",
        duration=60,
        style="educational"
    )
    
    print(f"Video generated: {video_path}")

# Run the application
asyncio.run(main())
```

### Command Line Interface

```bash
# Generate video from topic
faceless-video-ai --topic "Machine Learning" --duration 60 --style educational

# Generate from custom script
faceless-video-ai --script "path/to/script.txt" --style modern

# Batch generation
faceless-video-ai --batch topics.txt --duration 45
```

### Advanced Configuration

```python
from faceless_video_ai.config import Config, TTSConfig, VideoConfig

# Custom configuration
config = Config()
config.tts.engine = "whisperspeech"
config.tts.quality = "high"
config.video.resolution = (3840, 2160)  # 4K
config.video.use_libopenshot = True

# Initialize with custom config
fvai = FacelessVideoAI(config)
```

## 🏗️ Architecture

The Faceless Video AI system is built with a modular, component-based architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    FacelessVideoAI                         │
│                     (Main Controller)                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐   ┌────▼────┐   ┌────▼────┐
│Content │   │  TTS    │   │ Video   │
│Generator│   │ Engine  │   │Composer │
└───────┘   └─────────┘   └─────────┘
    │             │             │
    │             │             │
┌───▼───┐   ┌────▼────┐   ┌────▼────┐
│AI     │   │Multiple │   │libopenshot│
│Models │   │TTS      │   │MoviePy   │
│       │   │Engines  │   │          │
└───────┘   └─────────┘   └─────────┘
```

## 🔧 Configuration

### Environment Variables

```bash
# TTS Configuration
export TTS_ENGINE=whisperspeech
export TTS_QUALITY=high

# Video Configuration
export VIDEO_RESOLUTION=1920x1080
export USE_GPU=true

# API Keys (optional)
export OPENAI_API_KEY=your_openai_key
export UNSPLASH_API_KEY=your_unsplash_key
```

### Configuration File

Create `config.yaml`:

```yaml
tts:
  engine: whisperspeech
  quality: high
  language: en

video:
  resolution: [1920, 1080]
  fps: 30
  codec: libx264
  use_libopenshot: true

content:
  model: gpt-3.5-turbo
  default_style: educational
  include_subtitles: true

system:
  max_concurrent_jobs: 4
  use_gpu: true
  temp_dir: /tmp/faceless_video_ai
```

## 📚 Examples

### Example 1: Educational Video

```python
# Generate educational content about climate change
video_path = await fvai.generate_video_from_topic(
    topic="Climate Change Solutions",
    duration=90,
    style="educational",
    target_audience="high school students",
    tone="informative"
)
```

### Example 2: Custom Script

```python
# Create video from existing script
script = """
Welcome to our tutorial on Python programming!
Today we'll learn about functions and classes.
Let's start with the basics...
"""

video_path = await fvai.generate_video_from_script(
    script=script,
    visual_style="modern"
)
```

### Example 3: Batch Processing

```python
# Generate multiple videos
topics = [
    "Machine Learning Basics",
    "Data Science Fundamentals",
    "AI Ethics and Responsibility"
]

videos = await fvai.batch_generate_videos(
    topics=topics,
    duration=60,
    style="educational"
)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=faceless_video_ai

# Run specific test categories
pytest tests/test_tts.py
pytest tests/test_video.py
pytest tests/test_content.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/facelessvideoai/faceless-video-ai.git
cd faceless-video-ai

# Install development dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install

# Run linting
black .
flake8 .
mypy .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **WhisperSpeech** - High-quality TTS engine
- **libopenshot** - Professional video editing library
- **Stable Diffusion** - AI image generation
- **OpenAI** - Content generation models
- **Open Source Community** - For all the amazing tools and libraries

## 📞 Support

- **Documentation**: [https://docs.facelessvideoai.com/](https://docs.facelessvideoai.com/)
- **Issues**: [GitHub Issues](https://github.com/facelessvideoai/faceless-video-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/facelessvideoai/faceless-video-ai/discussions)
- **Email**: team@facelessvideoai.com

## 🚀 Roadmap

- [ ] **Real-time Video Generation**: Live streaming capabilities
- [ ] **Advanced AI Models**: Integration with cutting-edge AI research
- [ ] **Multi-Platform Support**: Web interface and mobile apps
- [ ] **Collaborative Features**: Team-based video creation
- [ ] **Analytics Dashboard**: Performance metrics and insights
- [ ] **Plugin Marketplace**: Third-party extensions and integrations

---

**Made with ❤️ by the Open Source Community**

*Faceless Video AI - Democratizing professional video creation through open-source innovation.*
