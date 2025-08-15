"""
Text-to-Speech engine integrating multiple open-source TTS solutions.
"""

import asyncio
import logging
import tempfile
from pathlib import Path
from typing import Dict, Optional, Union
import torch

from .config import TTSConfig


class TTSEngine:
    """
    High-quality TTS engine supporting multiple open-source solutions.
    
    Integrates WhisperSpeech, Piper, and XTTS for maximum quality and flexibility.
    """
    
    def __init__(self, config: TTSConfig):
        """Initialize the TTS engine with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize engines based on configuration
        self.engines = {}
        self._initialize_engines()
        
        self.logger.info(f"TTS Engine initialized with {self.config.engine}")
    
    def _initialize_engines(self):
        """Initialize available TTS engines."""
        try:
            # Initialize WhisperSpeech
            if self._can_import_whisperspeech():
                self.engines["whisperspeech"] = self._init_whisperspeech()
                self.logger.info("WhisperSpeech engine initialized")
            
            # Initialize Piper
            if self._can_import_piper():
                self.engines["piper"] = self._init_piper()
                self.logger.info("Piper engine initialized")
            
            # Initialize XTTS
            if self._can_import_xtts():
                self.engines["xtts"] = self._init_xtts()
                self.logger.info("XTTS engine initialized")
                
        except Exception as e:
            self.logger.warning(f"Failed to initialize some TTS engines: {e}")
    
    def _can_import_whisperspeech(self) -> bool:
        """Check if WhisperSpeech can be imported."""
        try:
            import whisperspeech
            return True
        except ImportError:
            self.logger.warning("WhisperSpeech not available")
            return False
    
    def _can_import_piper(self) -> bool:
        """Check if Piper can be imported."""
        try:
            import piper
            return True
        except ImportError:
            self.logger.warning("Piper not available")
            return False
    
    def _can_import_xtts(self) -> bool:
        """Check if XTTS can be imported."""
        try:
            from TTS.api import TTS
            return True
        except ImportError:
            self.logger.warning("XTTS not available")
            return False
    
    def _init_whisperspeech(self):
        """Initialize WhisperSpeech engine."""
        try:
            import whisperspeech
            
            # Configure device
            device = self.config.whisperspeech_device
            if device == "auto":
                device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # Load model
            model = whisperspeech.load_model(
                self.config.whisperspeech_model,
                device=device
            )
            
            return {
                "model": model,
                "device": device,
                "type": "whisperspeech"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WhisperSpeech: {e}")
            return None
    
    def _init_piper(self):
        """Initialize Piper engine."""
        try:
            import piper
            
            # Use default model if none specified
            model_path = self.config.piper_model_path or "en_US-amy-low.onnx"
            config_path = self.config.piper_config_path or "en_US-amy-low.onnx.json"
            
            # Initialize Piper
            piper_tts = piper.PiperVoice.load(
                model_path=model_path,
                config_path=config_path
            )
            
            return {
                "model": piper_tts,
                "type": "piper"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Piper: {e}")
            return None
    
    def _init_xtts(self):
        """Initialize XTTS engine."""
        try:
            from TTS.api import TTS
            
            # Initialize XTTS model
            tts = TTS(
                model_name=self.config.xtts_model,
                progress_bar=False
            )
            
            return {
                "model": tts,
                "type": "xtts"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to initialize XTTS: {e}")
            return None
    
    async def generate_speech(
        self,
        text: str,
        voice: Optional[str] = None,
        output_path: Optional[Union[str, Path]] = None,
        engine: Optional[str] = None
    ) -> Path:
        """
        Generate speech from text using the specified TTS engine.
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (engine-specific)
            output_path: Path to save the audio file
            engine: TTS engine to use (defaults to config)
            
        Returns:
            Path to the generated audio file
        """
        engine = engine or self.config.engine
        
        if engine not in self.engines:
            raise ValueError(f"TTS engine '{engine}' not available")
        
        if not self.engines[engine]:
            raise RuntimeError(f"TTS engine '{engine}' failed to initialize")
        
        self.logger.info(f"Generating speech using {engine} engine")
        
        try:
            if engine == "whisperspeech":
                return await self._generate_whisperspeech(text, voice, output_path)
            elif engine == "piper":
                return await self._generate_piper(text, voice, output_path)
            elif engine == "xtts":
                return await self._generate_xtts(text, voice, output_path)
            else:
                raise ValueError(f"Unknown TTS engine: {engine}")
                
        except Exception as e:
            self.logger.error(f"Speech generation failed: {e}")
            raise
    
    async def _generate_whisperspeech(
        self,
        text: str,
        voice: Optional[str],
        output_path: Optional[Union[str, Path]]
    ) -> Path:
        """Generate speech using WhisperSpeech."""
        engine_info = self.engines["whisperspeech"]
        model = engine_info["model"]
        
        # Generate audio
        audio = model.generate(text)
        
        # Save to file
        if output_path is None:
            output_path = Path(tempfile.mktemp(suffix=".wav"))
        
        output_path = Path(output_path)
        
        # Convert to numpy array and save
        import numpy as np
        import soundfile as sf
        
        audio_np = audio.cpu().numpy()
        sf.write(str(output_path), audio_np, 22050)
        
        return output_path
    
    async def _generate_piper(
        self,
        text: str,
        voice: Optional[str],
        output_path: Optional[Union[str, Path]]
    ) -> Path:
        """Generate speech using Piper."""
        engine_info = self.engines["piper"]
        model = engine_info["model"]
        
        # Generate audio
        audio = model.synthesize(text)
        
        # Save to file
        if output_path is None:
            output_path = Path(tempfile.mktemp(suffix=".wav"))
        
        output_path = Path(output_path)
        
        # Save audio
        with open(output_path, "wb") as f:
            f.write(audio)
        
        return output_path
    
    async def _generate_xtts(
        self,
        text: str,
        voice: Optional[str],
        output_path: Optional[Union[str, Path]]
    ) -> Path:
        """Generate speech using XTTS."""
        engine_info = self.engines["xtts"]
        model = engine_info["model"]
        
        # Save to file
        if output_path is None:
            output_path = Path(tempfile.mktemp(suffix=".wav"))
        
        output_path = Path(output_path)
        
        # Generate and save audio
        model.tts_to_file(
            text=text,
            file_path=str(output_path),
            speaker_wav=voice if voice else None
        )
        
        return output_path
    
    def get_available_voices(self, engine: Optional[str] = None) -> Dict[str, list]:
        """Get available voices for each engine."""
        engine = engine or self.config.engine
        
        voices = {}
        
        if engine == "whisperspeech" and "whisperspeech" in self.engines:
            voices["whisperspeech"] = ["librelight", "default"]
        
        elif engine == "piper" and "piper" in self.engines:
            voices["piper"] = ["en_US-amy-low", "en_US-amy-medium", "en_US-amy-high"]
        
        elif engine == "xtts" and "xtts" in self.engines:
            voices["xtts"] = ["default", "custom"]
        
        return voices
    
    def get_status(self) -> Dict:
        """Get the current status of the TTS engine."""
        return {
            "active_engine": self.config.engine,
            "available_engines": list(self.engines.keys()),
            "engine_status": {
                name: info is not None for name, info in self.engines.items()
            },
            "config": {
                "voice": self.config.voice,
                "speed": self.config.speed,
                "quality": self.config.quality,
                "language": self.config.language
            }
        }