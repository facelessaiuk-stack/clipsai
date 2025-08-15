"""
Faceless Video AI - Market-Leading Open-Source Faceless Video Software

A comprehensive solution for automated faceless video creation using exclusively
open-source components including AI-powered content generation, high-quality TTS,
and professional video composition.
"""

__version__ = "1.0.0"
__author__ = "Faceless Video AI Team"
__license__ = "MIT"

from .core import FacelessVideoAI
from .generators import ContentGenerator, VideoGenerator
from .tts import TTSEngine
from .video import VideoComposer

__all__ = [
    "FacelessVideoAI",
    "ContentGenerator", 
    "VideoGenerator",
    "TTSEngine",
    "VideoComposer"
]