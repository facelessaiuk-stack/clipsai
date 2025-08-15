"""
Core FacelessVideoAI class that orchestrates the entire video generation pipeline.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

from .generators import ContentGenerator, VideoGenerator
from .tts import TTSEngine
from .video import VideoComposer
from .config import Config


class FacelessVideoAI:
    """
    Main class for the Faceless Video AI application.
    
    This class orchestrates the entire pipeline from content generation to final video output,
    integrating all open-source components for maximum quality and efficiency.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the FacelessVideoAI system."""
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        
        # Initialize core components
        self.content_generator = ContentGenerator(self.config)
        self.tts_engine = TTSEngine(self.config)
        self.video_composer = VideoComposer(self.config)
        self.video_generator = VideoGenerator(self.config)
        
        self.logger.info("FacelessVideoAI initialized successfully")
    
    async def generate_video_from_topic(
        self, 
        topic: str, 
        duration: int = 60,
        style: str = "educational",
        output_path: Optional[Union[str, Path]] = None
    ) -> Path:
        """
        Generate a complete faceless video from a topic.
        
        Args:
            topic: The main topic/subject for the video
            duration: Target duration in seconds
            style: Content style (educational, entertainment, news, etc.)
            output_path: Optional custom output path
            
        Returns:
            Path to the generated video file
        """
        self.logger.info(f"Starting video generation for topic: {topic}")
        
        try:
            # Step 1: Generate content (script, key points, visual elements)
            content = await self.content_generator.generate_content(
                topic=topic,
                duration=duration,
                style=style
            )
            
            # Step 2: Generate speech from script
            audio_path = await self.tts_engine.generate_speech(
                text=content.script,
                voice=content.voice_preferences,
                output_path=output_path
            )
            
            # Step 3: Generate or gather visual assets
            visual_assets = await self.video_generator.generate_visuals(
                content=content,
                duration=duration
            )
            
            # Step 4: Compose final video
            video_path = await self.video_composer.compose_video(
                audio_path=audio_path,
                visual_assets=visual_assets,
                content=content,
                output_path=output_path
            )
            
            self.logger.info(f"Video generation completed: {video_path}")
            return video_path
            
        except Exception as e:
            self.logger.error(f"Video generation failed: {str(e)}")
            raise
    
    async def generate_video_from_script(
        self,
        script: str,
        visual_style: str = "modern",
        output_path: Optional[Union[str, Path]] = None
    ) -> Path:
        """
        Generate video from an existing script.
        
        Args:
            script: Pre-written script content
            visual_style: Visual presentation style
            output_path: Optional custom output path
            
        Returns:
            Path to the generated video file
        """
        self.logger.info("Starting video generation from script")
        
        try:
            # Generate speech from script
            audio_path = await self.tts_engine.generate_speech(
                text=script,
                voice="default",
                output_path=output_path
            )
            
            # Generate visual assets based on script content
            visual_assets = await self.video_generator.generate_visuals_from_script(
                script=script,
                style=visual_style
            )
            
            # Compose final video
            video_path = await self.video_composer.compose_video(
                audio_path=audio_path,
                visual_assets=visual_assets,
                content=None,
                output_path=output_path
            )
            
            self.logger.info(f"Video generation from script completed: {video_path}")
            return video_path
            
        except Exception as e:
            self.logger.error(f"Video generation from script failed: {str(e)}")
            raise
    
    async def batch_generate_videos(
        self,
        topics: List[str],
        duration: int = 60,
        style: str = "educational",
        output_dir: Optional[Union[str, Path]] = None
    ) -> List[Path]:
        """
        Generate multiple videos in batch.
        
        Args:
            topics: List of topics to generate videos for
            duration: Target duration for each video
            style: Content style for all videos
            output_dir: Directory to save generated videos
            
        Returns:
            List of paths to generated video files
        """
        self.logger.info(f"Starting batch generation of {len(topics)} videos")
        
        output_dir = Path(output_dir) if output_dir else Path("generated_videos")
        output_dir.mkdir(exist_ok=True)
        
        video_paths = []
        
        for i, topic in enumerate(topics):
            try:
                output_path = output_dir / f"video_{i+1:03d}_{topic.replace(' ', '_')}.mp4"
                video_path = await self.generate_video_from_topic(
                    topic=topic,
                    duration=duration,
                    style=style,
                    output_path=output_path
                )
                video_paths.append(video_path)
                
            except Exception as e:
                self.logger.error(f"Failed to generate video for topic '{topic}': {str(e)}")
                continue
        
        self.logger.info(f"Batch generation completed: {len(video_paths)} videos generated")
        return video_paths
    
    def get_system_status(self) -> Dict:
        """Get the current status of all system components."""
        return {
            "content_generator": self.content_generator.get_status(),
            "tts_engine": self.tts_engine.get_status(),
            "video_composer": self.video_composer.get_status(),
            "video_generator": self.video_generator.get_status(),
            "config": self.config.get_status()
        }