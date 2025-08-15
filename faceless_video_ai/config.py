"""
Configuration management for the Faceless Video AI system.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class TTSConfig:
    """Configuration for Text-to-Speech engines."""
    engine: str = "whisperspeech"  # whisperspeech, piper, xtts
    voice: str = "default"
    speed: float = 1.0
    quality: str = "high"  # low, medium, high
    language: str = "en"
    
    # WhisperSpeech specific
    whisperspeech_model: str = "librelight"
    whisperspeech_device: str = "auto"  # auto, cpu, cuda
    
    # Piper specific
    piper_model_path: Optional[str] = None
    piper_config_path: Optional[str] = None
    
    # XTTS specific
    xtts_model: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    xtts_voice_cloning: bool = True


@dataclass
class VideoConfig:
    """Configuration for video generation and composition."""
    resolution: tuple = (1920, 1080)
    fps: int = 30
    codec: str = "libx264"
    quality: str = "high"  # low, medium, high
    
    # OpenShot/libopenshot specific
    use_libopenshot: bool = True
    libopenshot_audio_effects: bool = True
    libopenshot_hardware_acceleration: bool = True
    
    # MoviePy fallback
    use_moviepy_fallback: bool = True
    
    # Visual generation
    image_style: str = "modern"
    transition_duration: float = 0.5
    background_music: bool = True
    background_music_path: Optional[str] = None


@dataclass
class ContentConfig:
    """Configuration for AI content generation."""
    model: str = "gpt-3.5-turbo"  # or local model path
    max_tokens: int = 2000
    temperature: float = 0.7
    creativity: float = 0.8
    
    # Content style preferences
    default_style: str = "educational"
    include_subtitles: bool = True
    subtitle_style: str = "modern"
    
    # Visual asset preferences
    image_source: str = "unsplash"  # unsplash, pexels, generated
    max_images_per_video: int = 10
    image_quality: str = "high"


@dataclass
class SystemConfig:
    """System-level configuration."""
    temp_dir: Path = field(default_factory=lambda: Path("/tmp/faceless_video_ai"))
    output_dir: Path = field(default_factory=lambda: Path("./generated_videos"))
    max_concurrent_jobs: int = 4
    log_level: str = "INFO"
    
    # Resource management
    max_memory_gb: int = 8
    max_gpu_memory_gb: int = 4
    use_gpu: bool = True
    
    # Caching
    enable_cache: bool = True
    cache_dir: Path = field(default_factory=lambda: Path("./cache"))
    cache_ttl_hours: int = 24


@dataclass
class Config:
    """Main configuration class for the Faceless Video AI system."""
    
    # Component configurations
    tts: TTSConfig = field(default_factory=TTSConfig)
    video: VideoConfig = field(default_factory=VideoConfig)
    content: ContentConfig = field(default_factory=ContentConfig)
    system: SystemConfig = field(default_factory=SystemConfig)
    
    # API keys and external services
    openai_api_key: Optional[str] = None
    unsplash_api_key: Optional[str] = None
    pexels_api_key: Optional[str] = None
    
    # Model paths for local models
    local_models_dir: Optional[Path] = None
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration with optional config file."""
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
        
        # Set environment variables
        self._load_from_env()
        
        # Create necessary directories
        self._create_directories()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.unsplash_api_key = os.getenv("UNSPLASH_API_KEY")
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")
        
        # TTS configuration
        if os.getenv("TTS_ENGINE"):
            self.tts.engine = os.getenv("TTS_ENGINE")
        
        # Video configuration
        if os.getenv("VIDEO_RESOLUTION"):
            res = os.getenv("VIDEO_RESOLUTION").split("x")
            if len(res) == 2:
                self.video.resolution = (int(res[0]), int(res[1]))
        
        # System configuration
        if os.getenv("MAX_CONCURRENT_JOBS"):
            self.system.max_concurrent_jobs = int(os.getenv("MAX_CONCURRENT_JOBS"))
        
        if os.getenv("USE_GPU"):
            self.system.use_gpu = os.getenv("USE_GPU").lower() == "true"
    
    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        self.system.temp_dir.mkdir(parents=True, exist_ok=True)
        self.system.output_dir.mkdir(parents=True, exist_ok=True)
        self.system.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def load_from_file(self, config_file: str):
        """Load configuration from a JSON or YAML file."""
        # Implementation for loading from config files
        pass
    
    def save_to_file(self, config_file: str):
        """Save current configuration to a file."""
        # Implementation for saving to config files
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current configuration status."""
        return {
            "tts_engine": self.tts.engine,
            "video_resolution": self.video.resolution,
            "content_model": self.content.model,
            "system_temp_dir": str(self.system.temp_dir),
            "system_output_dir": str(self.system.output_dir),
            "max_concurrent_jobs": self.system.max_concurrent_jobs,
            "use_gpu": self.system.use_gpu,
            "api_keys_configured": {
                "openai": bool(self.openai_api_key),
                "unsplash": bool(self.unsplash_api_key),
                "pexels": bool(self.pexels_api_key)
            }
        }
    
    def validate(self) -> bool:
        """Validate the current configuration."""
        # Check if required directories exist
        if not self.system.temp_dir.exists():
            return False
        
        # Check if TTS engine is valid
        valid_tts_engines = ["whisperspeech", "piper", "xtts"]
        if self.tts.engine not in valid_tts_engines:
            return False
        
        # Check if video codec is valid
        valid_codecs = ["libx264", "libx265", "h264_nvenc", "h265_nvenc"]
        if self.video.codec not in valid_codecs:
            return False
        
        return True