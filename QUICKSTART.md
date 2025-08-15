# ⚡ Quick Start Guide - Faceless Video AI

Get up and running with Faceless Video AI in under 10 minutes!

## 🚀 Super Quick Start

### 1. Clone and Install
```bash
# Clone the repository
git clone https://github.com/facelessvideoai/faceless-video-ai.git
cd faceless-video-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### 2. Generate Your First Video
```bash
# Generate a video about AI
python cli.py generate --topic "Artificial Intelligence" --duration 30 --style educational
```

### 3. Check the Output
```bash
# View generated video
ls -la output/
```

That's it! 🎉

## 📱 Command Line Interface

### Generate Videos from Topics
```bash
# Educational video
python cli.py generate --topic "Machine Learning" --duration 60 --style educational

# Entertainment video
python cli.py generate --topic "Space Exploration" --duration 45 --style entertainment

# Business video
python cli.py generate --topic "Digital Marketing" --duration 90 --style business
```

### Generate from Scripts
```bash
# Create a script file
echo "Welcome to our video about Python programming!" > my_script.txt

# Generate video from script
python cli.py script --script my_script.txt --style modern
```

### Batch Generation
```bash
# Create topics file
echo -e "Python Basics\nWeb Development\nData Science" > topics.txt

# Generate multiple videos
python cli.py batch --topics topics.txt --duration 45 --style educational
```

### System Status
```bash
# Check system health
python cli.py status

# Test the system
python cli.py test --topic "Test Video" --duration 20
```

## 🎯 Common Use Cases

### Educational Content
```bash
python cli.py generate \
  --topic "Climate Change Solutions" \
  --duration 90 \
  --style educational \
  --audience "high school students" \
  --tone informative
```

### Business Presentations
```bash
python cli.py generate \
  --topic "Digital Transformation" \
  --duration 120 \
  --style business \
  --audience "executives" \
  --tone formal
```

### Social Media Content
```bash
python cli.py generate \
  --topic "Quick Python Tips" \
  --duration 30 \
  --style entertainment \
  --audience "developers" \
  --tone casual
```

## ⚙️ Quick Configuration

### Environment Variables
```bash
# Set your preferences
export TTS_ENGINE=whisperspeech
export VIDEO_RESOLUTION=1920x1080
export USE_GPU=true

# Optional API keys
export OPENAI_API_KEY="your_key_here"
```

### Configuration File
```bash
# Generate config template
python cli.py config-gen --output my_config.yaml

# Use custom config
python cli.py --config my_config.yaml generate --topic "Test"
```

## 🔧 Troubleshooting

### Common Issues
```bash
# Check if everything is working
python cli.py status

# Test with minimal settings
python cli.py test --topic "Test" --duration 10

# Check logs
tail -f faceless_video_ai.log
```

### Performance Issues
```bash
# Reduce resource usage
export MAX_CONCURRENT_JOBS=1
export VIDEO_RESOLUTION=1280x720

# Use CPU only
export USE_GPU=false
```

## 📚 Next Steps

1. **Run the Demo**: `python examples/demo.py`
2. **Read Full Docs**: Check [README.md](README.md)
3. **Customize**: Modify configuration files
4. **Join Community**: Visit GitHub Discussions

## 🆘 Need Help?

- **Quick Issues**: Check this guide
- **Detailed Help**: See [INSTALL.md](INSTALL.md)
- **Community**: GitHub Discussions
- **Bugs**: GitHub Issues

---

**Ready to create amazing videos? Let's go! 🎬✨**