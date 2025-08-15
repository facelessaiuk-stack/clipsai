from setuptools import find_packages, setup

setup(
    name="faceless-video-ai",
    version="1.0.0",
    description=(
        "Market-Leading Open-Source Faceless Video Software - "
        "AI-powered content generation, high-quality TTS, and professional video composition"
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Faceless Video AI Team",
    author_email="team@facelessvideoai.com",
    url="https://github.com/facelessvideoai/faceless-video-ai",
    license="MIT",
    packages=find_packages(exclude=["tests*", "sandbox*"]),
    py_modules=["main"],
    install_requires=[
        # Core dependencies
        "python-magic>=0.4.27",
        "numpy>=1.21.0",
        "pillow>=9.0.0",
        "pathlib2>=2.3.7",
        
        # Audio and Video Processing
        "librosa>=0.9.0",
        "soundfile>=0.10.3",
        "ffmpeg-python>=0.2.0",
        "opencv-python>=4.5.0",
        "av>=9.0.0",
        
        # Text-to-Speech Engines
        "whisperspeech>=0.1.0",
        "piper-tts>=1.0.0",
        "TTS>=0.13.0",
        
        # Video Composition
        "openshot-qt>=2.6.0",
        "libopenshot>=0.2.0",
        "moviepy>=1.0.3",
        
        # AI and Machine Learning
        "torch>=1.12.0",
        "torchaudio>=0.12.0",
        "transformers>=4.20.0",
        "diffusers>=0.10.0",
        "accelerate>=0.15.0",
        
        # Utilities
        "requests>=2.28.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=0.19.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "rich>=12.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.950",
        ],
        "openai": [
            "openai>=0.27.0",
        ],
        "gpu": [
            "cuda-python>=11.7.0",
            "cupy-cuda11x>=11.0.0",
        ],
        "full": [
            "stability-sdk>=0.8.0",
            "nltk>=3.7",
            "sentence-transformers>=2.2.0",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Content Creators",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Documentation": "https://docs.facelessvideoai.com/",
        "Homepage": "https://facelessvideoai.com/",
        "Repository": "https://github.com/facelessvideoai/faceless-video-ai",
        "Issues": "https://github.com/facelessvideoai/faceless-video-ai/issues",
        "Discussions": "https://github.com/facelessvideoai/faceless-video-ai/discussions",
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "faceless-video-ai=main:main",
            "fvai=main:main",
        ],
    },
    keywords=[
        "faceless video",
        "ai video generation",
        "text-to-speech",
        "video composition",
        "content creation",
        "automated video",
        "open source",
        "machine learning",
        "artificial intelligence",
    ],
)
