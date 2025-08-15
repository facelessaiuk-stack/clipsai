"""
Video composition engine integrating libopenshot and MoviePy for professional video creation.
"""

import asyncio
import logging
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

from .config import VideoConfig


@dataclass
class VisualAsset:
    """Represents a visual asset for video composition."""
    path: Path
    asset_type: str  # image, video, text, animation
    duration: float
    start_time: float = 0.0
    effects: Dict[str, Any] = None
    position: tuple = (0, 0)
    scale: float = 1.0
    opacity: float = 1.0


@dataclass
class VideoComposition:
    """Represents a complete video composition."""
    assets: List[VisualAsset]
    audio_path: Path
    duration: float
    resolution: tuple
    fps: int
    background_color: str = "#000000"
    transitions: List[Dict[str, Any]] = None


class VideoComposer:
    """
    Professional video composition engine using libopenshot and MoviePy.
    
    Provides high-quality video composition with advanced effects, transitions,
    and multi-layer compositing capabilities.
    """
    
    def __init__(self, config: VideoConfig):
        """Initialize the video composer with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize composition engines
        self.libopenshot_available = self._check_libopenshot()
        self.moviepy_available = self._check_moviepy()
        
        if not self.libopenshot_available and not self.moviepy_available:
            raise RuntimeError("No video composition engine available")
        
        self.logger.info(f"Video Composer initialized - libopenshot: {self.libopenshot_available}, moviepy: {self.moviepy_available}")
    
    def _check_libopenshot(self) -> bool:
        """Check if libopenshot is available."""
        try:
            import openshot
            return True
        except ImportError:
            self.logger.warning("libopenshot not available")
            return False
    
    def _check_moviepy(self) -> bool:
        """Check if MoviePy is available."""
        try:
            import moviepy.editor as mp
            return True
        except ImportError:
            self.logger.warning("MoviePy not available")
            return False
    
    async def compose_video(
        self,
        audio_path: Union[str, Path],
        visual_assets: List[VisualAsset],
        content: Optional[Any] = None,
        output_path: Optional[Union[str, Path]] = None,
        composition: Optional[VideoComposition] = None
    ) -> Path:
        """
        Compose a complete video from audio and visual assets.
        
        Args:
            audio_path: Path to the audio file
            visual_assets: List of visual assets to include
            content: Optional content metadata
            output_path: Path to save the final video
            composition: Optional pre-defined composition
            
        Returns:
            Path to the generated video file
        """
        if output_path is None:
            output_path = Path(tempfile.mktemp(suffix=".mp4"))
        
        output_path = Path(output_path)
        
        # Create composition if not provided
        if composition is None:
            composition = self._create_composition(audio_path, visual_assets)
        
        self.logger.info(f"Starting video composition with {len(visual_assets)} assets")
        
        try:
            # Try libopenshot first for highest quality
            if self.libopenshot_available and self.config.use_libopenshot:
                return await self._compose_with_libopenshot(composition, output_path)
            
            # Fallback to MoviePy
            elif self.moviepy_available and self.config.use_moviepy_fallback:
                return await self._compose_with_moviepy(composition, output_path)
            
            else:
                raise RuntimeError("No video composition engine available")
                
        except Exception as e:
            self.logger.error(f"Video composition failed: {e}")
            raise
    
    def _create_composition(
        self,
        audio_path: Union[str, Path],
        visual_assets: List[VisualAsset]
    ) -> VideoComposition:
        """Create a video composition from assets."""
        # Calculate total duration from audio
        import librosa
        duration = librosa.get_duration(path=str(audio_path))
        
        # Create composition
        composition = VideoComposition(
            assets=visual_assets,
            audio_path=Path(audio_path),
            duration=duration,
            resolution=self.config.resolution,
            fps=self.config.fps,
            background_color="#000000",
            transitions=[]
        )
        
        return composition
    
    async def _compose_with_libopenshot(
        self,
        composition: VideoComposition,
        output_path: Path
    ) -> Path:
        """Compose video using libopenshot for maximum quality."""
        try:
            import openshot
            
            # Create project
            project = openshot.Project()
            project.SetSetting("width", str(composition.resolution[0]))
            project.SetSetting("height", str(composition.resolution[1]))
            project.SetSetting("fps", str(composition.fps))
            
            # Add audio track
            audio_clip = openshot.Clip(str(composition.audio_path))
            audio_track = openshot.Track()
            audio_track.AddClip(audio_clip)
            project.AddTrack(audio_track)
            
            # Add visual tracks
            for i, asset in enumerate(composition.assets):
                track = openshot.Track()
                
                # Create clip from asset
                clip = openshot.Clip(str(asset.path))
                clip.Start(asset.start_time)
                clip.End(asset.start_time + asset.duration)
                
                # Apply effects
                if asset.effects:
                    for effect_name, effect_params in asset.effects.items():
                        effect = self._create_libopenshot_effect(effect_name, effect_params)
                        if effect:
                            clip.AddEffect(effect)
                
                # Apply transformations
                clip.ScaleX(asset.scale)
                clip.ScaleY(asset.scale)
                clip.LocationX(asset.position[0])
                clip.LocationY(asset.position[1])
                
                track.AddClip(clip)
                project.AddTrack(track)
            
            # Export video
            project.Export(str(output_path), "mp4")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"libopenshot composition failed: {e}")
            raise
    
    async def _compose_with_moviepy(
        self,
        composition: VideoComposition,
        output_path: Path
    ) -> Path:
        """Compose video using MoviePy as fallback."""
        try:
            import moviepy.editor as mp
            from moviepy.video.fx import resize, fadein, fadeout
            
            # Load audio
            audio = mp.AudioFileClip(str(composition.audio_path))
            
            # Create video clips from assets
            video_clips = []
            
            for asset in composition.assets:
                if asset.asset_type == "image":
                    # Create image clip
                    clip = mp.ImageClip(str(asset.path), duration=asset.duration)
                    clip = clip.set_start(asset.start_time)
                    
                    # Apply transformations
                    if asset.scale != 1.0:
                        clip = clip.resize(asset.scale)
                    
                    if asset.opacity != 1.0:
                        clip = clip.set_opacity(asset.opacity)
                    
                    # Position clip
                    clip = clip.set_position(asset.position)
                    
                    video_clips.append(clip)
                
                elif asset.asset_type == "video":
                    # Load video clip
                    clip = mp.VideoFileClip(str(asset.path))
                    clip = clip.set_duration(asset.duration)
                    clip = clip.set_start(asset.start_time)
                    
                    # Apply transformations
                    if asset.scale != 1.0:
                        clip = clip.resize(asset.scale)
                    
                    if asset.opacity != 1.0:
                        clip = clip.set_opacity(asset.opacity)
                    
                    # Position clip
                    clip = clip.set_position(asset.position)
                    
                    video_clips.append(clip)
                
                elif asset.asset_type == "text":
                    # Create text clip
                    clip = mp.TextClip(
                        asset.path,  # Text content
                        fontsize=70,
                        color='white',
                        font='Arial-Bold'
                    )
                    clip = clip.set_duration(asset.duration)
                    clip = clip.set_start(asset.start_time)
                    clip = clip.set_position(asset.position)
                    
                    video_clips.append(clip)
            
            # Composite all clips
            if video_clips:
                final_video = mp.CompositeVideoClip(
                    video_clips,
                    size=composition.resolution
                )
            else:
                # Create blank video if no visual assets
                final_video = mp.ColorClip(
                    size=composition.resolution,
                    color=composition.background_color,
                    duration=composition.duration
                )
            
            # Add audio
            final_video = final_video.set_audio(audio)
            
            # Write final video
            final_video.write_videofile(
                str(output_path),
                fps=composition.fps,
                codec=self.config.codec,
                audio_codec='aac'
            )
            
            # Clean up
            final_video.close()
            audio.close()
            for clip in video_clips:
                clip.close()
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"MoviePy composition failed: {e}")
            raise
    
    def _create_libopenshot_effect(self, effect_name: str, effect_params: Dict[str, Any]):
        """Create a libopenshot effect with parameters."""
        try:
            import openshot
            
            if effect_name == "fade_in":
                effect = openshot.FadeIn()
                if "duration" in effect_params:
                    effect.Duration(effect_params["duration"])
                return effect
            
            elif effect_name == "fade_out":
                effect = openshot.FadeOut()
                if "duration" in effect_params:
                    effect.Duration(effect_params["duration"])
                return effect
            
            elif effect_name == "blur":
                effect = openshot.Blur()
                if "amount" in effect_params:
                    effect.Amount(effect_params["amount"])
                return effect
            
            elif effect_name == "brightness":
                effect = openshot.Brightness()
                if "value" in effect_params:
                    effect.Value(effect_params["value"])
                return effect
            
            # Add more effects as needed
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Failed to create effect {effect_name}: {e}")
            return None
    
    async def add_transitions(
        self,
        video_path: Union[str, Path],
        transitions: List[Dict[str, Any]],
        output_path: Optional[Union[str, Path]] = None
    ) -> Path:
        """Add transitions between video segments."""
        # Implementation for adding transitions
        pass
    
    async def add_subtitles(
        self,
        video_path: Union[str, Path],
        subtitles: List[Dict[str, Any]],
        output_path: Optional[Union[str, Path]] = None
    ) -> Path:
        """Add subtitles to the video."""
        # Implementation for adding subtitles
        pass
    
    def get_status(self) -> Dict:
        """Get the current status of the video composer."""
        return {
            "libopenshot_available": self.libopenshot_available,
            "moviepy_available": self.moviepy_available,
            "preferred_engine": "libopenshot" if self.config.use_libopenshot else "moviepy",
            "resolution": self.config.resolution,
            "fps": self.config.fps,
            "codec": self.config.codec,
            "hardware_acceleration": self.config.libopenshot_hardware_acceleration
        }