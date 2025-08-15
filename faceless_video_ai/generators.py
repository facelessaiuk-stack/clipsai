"""
Content and video generators for AI-powered faceless video creation.
"""

import asyncio
import logging
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import json

from .config import ContentConfig, VideoConfig
from .video import VisualAsset


@dataclass
class GeneratedContent:
    """Represents AI-generated content for video creation."""
    topic: str
    script: str
    key_points: List[str]
    visual_elements: List[str]
    voice_preferences: Dict[str, Any]
    style: str
    duration: int
    target_audience: str
    tone: str  # formal, casual, educational, entertaining


@dataclass
class GeneratedVisuals:
    """Represents generated visual assets for video composition."""
    images: List[Path]
    animations: List[Path]
    text_overlays: List[Dict[str, Any]]
    background_elements: List[Path]
    transitions: List[Dict[str, Any]]


class ContentGenerator:
    """
    AI-powered content generator for creating video scripts and content structure.
    
    Integrates with various AI models to generate engaging, structured content
    for faceless videos.
    """
    
    def __init__(self, config: ContentConfig):
        """Initialize the content generator with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize AI models
        self.openai_available = self._check_openai()
        self.local_models_available = self._check_local_models()
        
        self.logger.info(f"Content Generator initialized - OpenAI: {self.openai_available}, Local: {self.local_models_available}")
    
    def _check_openai(self) -> bool:
        """Check if OpenAI API is available."""
        try:
            import openai
            return True
        except ImportError:
            return False
    
    def _check_local_models(self) -> bool:
        """Check if local AI models are available."""
        try:
            from transformers import pipeline
            return True
        except ImportError:
            return False
    
    async def generate_content(
        self,
        topic: str,
        duration: int = 60,
        style: str = "educational",
        target_audience: str = "general",
        tone: str = "informative"
    ) -> GeneratedContent:
        """
        Generate complete content for a faceless video.
        
        Args:
            topic: Main topic/subject
            duration: Target duration in seconds
            style: Content style (educational, entertainment, news, etc.)
            target_audience: Target audience description
            tone: Desired tone for the content
            
        Returns:
            GeneratedContent object with script and visual elements
        """
        self.logger.info(f"Generating content for topic: {topic}")
        
        try:
            # Generate script
            script = await self._generate_script(topic, duration, style, target_audience, tone)
            
            # Extract key points
            key_points = await self._extract_key_points(script)
            
            # Generate visual elements
            visual_elements = await self._generate_visual_elements(topic, key_points, style)
            
            # Determine voice preferences
            voice_preferences = self._determine_voice_preferences(style, tone, target_audience)
            
            # Create content object
            content = GeneratedContent(
                topic=topic,
                script=script,
                key_points=key_points,
                visual_elements=visual_elements,
                voice_preferences=voice_preferences,
                style=style,
                duration=duration,
                target_audience=target_audience,
                tone=tone
            )
            
            self.logger.info(f"Content generation completed for topic: {topic}")
            return content
            
        except Exception as e:
            self.logger.error(f"Content generation failed: {e}")
            raise
    
    async def _generate_script(
        self,
        topic: str,
        duration: int,
        style: str,
        target_audience: str,
        tone: str
    ) -> str:
        """Generate a video script using AI."""
        if self.openai_available:
            return await self._generate_script_openai(topic, duration, style, target_audience, tone)
        elif self.local_models_available:
            return await self._generate_script_local(topic, duration, style, target_audience, tone)
        else:
            # Fallback to template-based generation
            return self._generate_script_template(topic, duration, style, target_audience, tone)
    
    async def _generate_script_openai(
        self,
        topic: str,
        duration: int,
        style: str,
        target_audience: str,
        tone: str
    ) -> str:
        """Generate script using OpenAI API."""
        try:
            import openai
            
            prompt = f"""
            Create a {duration}-second faceless video script about "{topic}" in a {style} style.
            
            Target audience: {target_audience}
            Tone: {tone}
            
            Requirements:
            - Engaging opening hook
            - Clear structure with 3-5 main points
            - Conversational language suitable for voice-over
            - Include specific examples and data points
            - Strong conclusion with call-to-action
            
            Format the script with clear timing markers and speaker notes.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are an expert video script writer specializing in faceless videos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"OpenAI script generation failed: {e}")
            raise
    
    async def _generate_script_local(
        self,
        topic: str,
        duration: int,
        style: str,
        target_audience: str,
        tone: str
    ) -> str:
        """Generate script using local AI models."""
        try:
            from transformers import pipeline
            
            # Use text generation pipeline
            generator = pipeline("text-generation", model="gpt2")
            
            prompt = f"Create a {duration}-second video script about {topic} in {style} style for {target_audience} audience with {tone} tone."
            
            result = generator(prompt, max_length=200, num_return_sequences=1)
            
            return result[0]['generated_text']
            
        except Exception as e:
            self.logger.error(f"Local model script generation failed: {e}")
            raise
    
    def _generate_script_template(
        self,
        topic: str,
        duration: int,
        style: str,
        target_audience: str,
        tone: str
    ) -> str:
        """Generate script using template-based approach."""
        # Simple template-based script generation
        script = f"""
        [Opening - 0:00-0:10]
        Welcome to our video about {topic}. Today, we'll explore the key aspects that make this topic fascinating and important.
        
        [Main Content - 0:10-{duration-10}]
        Let's dive into the main points about {topic}:
        
        1. First, let's understand the basics
        2. Next, we'll explore the key benefits
        3. Finally, we'll look at practical applications
        
        [Conclusion - {duration-10}-{duration}]
        That concludes our exploration of {topic}. Thank you for watching!
        """
        
        return script.strip()
    
    async def _extract_key_points(self, script: str) -> List[str]:
        """Extract key points from the generated script."""
        # Simple extraction - split by sentences and identify key points
        sentences = script.split('.')
        key_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 20:  # Filter out very short sentences
                key_points.append(sentence)
        
        return key_points[:5]  # Limit to 5 key points
    
    async def _generate_visual_elements(
        self,
        topic: str,
        key_points: List[str],
        style: str
    ) -> List[str]:
        """Generate visual element descriptions for the video."""
        visual_elements = []
        
        # Add topic-related visuals
        visual_elements.append(f"Main topic: {topic}")
        
        # Add visuals for each key point
        for i, point in enumerate(key_points[:3]):  # Limit to 3 visual elements
            visual_elements.append(f"Key point {i+1}: {point[:50]}...")
        
        # Add style-specific visuals
        if style == "educational":
            visual_elements.extend(["Infographics", "Charts and graphs", "Step-by-step diagrams"])
        elif style == "entertainment":
            visual_elements.extend(["Dynamic animations", "Colorful graphics", "Engaging transitions"])
        elif style == "news":
            visual_elements.extend(["Professional graphics", "Data visualizations", "Clean layouts"])
        
        return visual_elements
    
    def _determine_voice_preferences(
        self,
        style: str,
        tone: str,
        target_audience: str
    ) -> Dict[str, Any]:
        """Determine optimal voice preferences based on content characteristics."""
        preferences = {
            "speed": 1.0,
            "pitch": "medium",
            "clarity": "high"
        }
        
        # Adjust based on style
        if style == "educational":
            preferences["speed"] = 0.9  # Slightly slower for learning
            preferences["clarity"] = "very_high"
        elif style == "entertainment":
            preferences["speed"] = 1.1  # Slightly faster for engagement
            preferences["pitch"] = "varied"
        
        # Adjust based on tone
        if tone == "formal":
            preferences["pitch"] = "low"
        elif tone == "casual":
            preferences["pitch"] = "medium_high"
        
        return preferences
    
    def get_status(self) -> Dict:
        """Get the current status of the content generator."""
        return {
            "openai_available": self.openai_available,
            "local_models_available": self.local_models_available,
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "default_style": self.config.default_style
        }


class VideoGenerator:
    """
    AI-powered video generator for creating visual assets and compositions.
    
    Integrates with image generation models and video creation tools to
    produce high-quality visual content for faceless videos.
    """
    
    def __init__(self, config: VideoConfig):
        """Initialize the video generator with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize generation capabilities
        self.image_generation_available = self._check_image_generation()
        self.video_generation_available = self._check_video_generation()
        
        self.logger.info(f"Video Generator initialized - Images: {self.image_generation_available}, Videos: {self.video_generation_available}")
    
    def _check_image_generation(self) -> bool:
        """Check if image generation is available."""
        try:
            # Check for various image generation libraries
            import diffusers
            return True
        except ImportError:
            try:
                import stability_sdk
                return True
            except ImportError:
                return False
    
    def _check_video_generation(self) -> bool:
        """Check if video generation is available."""
        try:
            # Check for video generation libraries
            import diffusers
            return True
        except ImportError:
            return False
    
    async def generate_visuals(
        self,
        content: GeneratedContent,
        duration: int
    ) -> GeneratedVisuals:
        """
        Generate visual assets for video composition.
        
        Args:
            content: Generated content object
            duration: Target video duration
            
        Returns:
            GeneratedVisuals object with all visual assets
        """
        self.logger.info(f"Generating visuals for {duration}s video")
        
        try:
            # Generate images based on content
            images = await self._generate_images(content.visual_elements, content.style)
            
            # Generate animations
            animations = await self._generate_animations(content.key_points, content.style)
            
            # Create text overlays
            text_overlays = await self._create_text_overlays(content.key_points, content.style)
            
            # Generate background elements
            background_elements = await self._generate_backgrounds(content.style, duration)
            
            # Create transitions
            transitions = self._create_transitions(len(content.key_points))
            
            # Create visuals object
            visuals = GeneratedVisuals(
                images=images,
                animations=animations,
                text_overlays=text_overlays,
                background_elements=background_elements,
                transitions=transitions
            )
            
            self.logger.info(f"Visual generation completed with {len(images)} images")
            return visuals
            
        except Exception as e:
            self.logger.error(f"Visual generation failed: {e}")
            raise
    
    async def generate_visuals_from_script(
        self,
        script: str,
        style: str
    ) -> GeneratedVisuals:
        """Generate visuals from an existing script."""
        # Parse script to extract key elements
        key_points = script.split('.')[:5]  # Simple parsing
        
        # Generate visuals based on script content
        images = await self._generate_images([f"Script element: {point[:30]}..." for point in key_points], style)
        animations = await self._generate_animations(key_points, style)
        text_overlays = await self._create_text_overlays(key_points, style)
        background_elements = await self._generate_backgrounds(style, 60)  # Default duration
        transitions = self._create_transitions(len(key_points))
        
        return GeneratedVisuals(
            images=images,
            animations=animations,
            text_overlays=text_overlays,
            background_elements=background_elements,
            transitions=transitions
        )
    
    async def _generate_images(
        self,
        descriptions: List[str],
        style: str
    ) -> List[Path]:
        """Generate images based on descriptions."""
        images = []
        
        for description in descriptions:
            try:
                image_path = await self._generate_single_image(description, style)
                if image_path:
                    images.append(image_path)
            except Exception as e:
                self.logger.warning(f"Failed to generate image for '{description}': {e}")
                continue
        
        return images
    
    async def _generate_single_image(self, description: str, style: str) -> Optional[Path]:
        """Generate a single image using AI models."""
        try:
            if self.image_generation_available:
                return await self._generate_with_diffusers(description, style)
            else:
                # Fallback to placeholder images
                return self._create_placeholder_image(description, style)
        except Exception as e:
            self.logger.error(f"Image generation failed: {e}")
            return None
    
    async def _generate_with_diffusers(self, description: str, style: str) -> Path:
        """Generate image using diffusers library."""
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            
            # Load model
            pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16
            )
            
            if torch.cuda.is_available():
                pipe = pipe.to("cuda")
            
            # Generate image
            prompt = f"{description}, {style} style, high quality, professional"
            image = pipe(prompt).images[0]
            
            # Save image
            output_path = Path(tempfile.mktemp(suffix=".png"))
            image.save(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Diffusers image generation failed: {e}")
            raise
    
    def _create_placeholder_image(self, description: str, style: str) -> Path:
        """Create a placeholder image when AI generation is not available."""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import random
            
            # Create a simple placeholder image
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color='#2c3e50')
            draw = ImageDraw.Draw(image)
            
            # Add text
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # Draw description text
            text = description[:50] + "..." if len(description) > 50 else description
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            draw.text((x, y), text, fill='white', font=font)
            
            # Save image
            output_path = Path(tempfile.mktemp(suffix=".png"))
            image.save(output_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Placeholder image creation failed: {e}")
            raise
    
    async def _generate_animations(
        self,
        key_points: List[str],
        style: str
    ) -> List[Path]:
        """Generate animations for key points."""
        # For now, return empty list - animation generation can be implemented later
        return []
    
    async def _create_text_overlays(
        self,
        key_points: List[str],
        style: str
    ) -> List[Dict[str, Any]]:
        """Create text overlay configurations."""
        overlays = []
        
        for i, point in enumerate(key_points):
            overlay = {
                "text": point[:100] + "..." if len(point) > 100 else point,
                "position": "center",
                "font_size": 48,
                "color": "#ffffff",
                "background": "#00000080",
                "start_time": i * 10,  # 10 seconds per point
                "duration": 8
            }
            overlays.append(overlay)
        
        return overlays
    
    async def _generate_backgrounds(self, style: str, duration: int) -> List[Path]:
        """Generate background elements."""
        # For now, return empty list - background generation can be implemented later
        return []
    
    def _create_transitions(self, num_segments: int) -> List[Dict[str, Any]]:
        """Create transition configurations."""
        transitions = []
        
        for i in range(num_segments - 1):
            transition = {
                "type": "fade",
                "duration": self.config.transition_duration,
                "start_time": (i + 1) * 10 - self.config.transition_duration / 2
            }
            transitions.append(transition)
        
        return transitions
    
    def get_status(self) -> Dict:
        """Get the current status of the video generator."""
        return {
            "image_generation_available": self.image_generation_available,
            "video_generation_available": self.video_generation_available,
            "image_style": self.config.image_style,
            "transition_duration": self.config.transition_duration,
            "background_music": self.config.background_music
        }