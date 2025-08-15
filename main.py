#!/usr/bin/env python3
"""
Faceless Video AI - Main Application Entry Point

A market-leading open-source faceless video software that integrates advanced AI
for content generation, high-quality TTS, and professional video composition.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the faceless_video_ai package to the path
sys.path.insert(0, str(Path(__file__).parent))

from faceless_video_ai import FacelessVideoAI
from faceless_video_ai.config import Config


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('faceless_video_ai.log')
        ]
    )


async def main():
    """Main application function."""
    print("🎬 Faceless Video AI - Market-Leading Open-Source Video Software")
    print("=" * 70)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize configuration
        config = Config()
        
        # Validate configuration
        if not config.validate():
            logger.error("Configuration validation failed")
            return
        
        # Initialize the Faceless Video AI system
        logger.info("Initializing Faceless Video AI system...")
        fvai = FacelessVideoAI(config)
        
        # Display system status
        status = fvai.get_system_status()
        print("\n📊 System Status:")
        print(f"  TTS Engine: {status['tts_engine']['active_engine']}")
        print(f"  Video Resolution: {status['video_resolution']}")
        print(f"  Content Model: {status['content_model']}")
        print(f"  GPU Available: {status['use_gpu']}")
        
        # Example usage
        print("\n🚀 Example: Generating a video about 'Artificial Intelligence'")
        
        # Generate video from topic
        video_path = await fvai.generate_video_from_topic(
            topic="Artificial Intelligence",
            duration=60,
            style="educational",
            output_path="./output/ai_introduction.mp4"
        )
        
        print(f"✅ Video generated successfully: {video_path}")
        
        # Example: Generate video from script
        print("\n📝 Example: Generating video from custom script")
        
        custom_script = """
        Welcome to our video about machine learning! 
        
        Machine learning is a subset of artificial intelligence that enables computers 
        to learn and improve from experience without being explicitly programmed. 
        It's revolutionizing industries from healthcare to finance.
        
        The key benefits include automation, pattern recognition, and predictive analytics. 
        Companies use ML to optimize operations, enhance customer experiences, and drive innovation.
        
        Thank you for watching our introduction to machine learning!
        """
        
        script_video_path = await fvai.generate_video_from_script(
            script=custom_script,
            visual_style="modern",
            output_path="./output/ml_script_video.mp4"
        )
        
        print(f"✅ Script-based video generated: {script_video_path}")
        
        # Example: Batch generation
        print("\n🔄 Example: Batch video generation")
        
        topics = [
            "Climate Change Solutions",
            "Space Exploration",
            "Renewable Energy"
        ]
        
        batch_videos = await fvai.batch_generate_videos(
            topics=topics,
            duration=45,
            style="educational",
            output_dir="./output/batch_videos"
        )
        
        print(f"✅ Batch generation completed: {len(batch_videos)} videos created")
        for video in batch_videos:
            print(f"  - {video.name}")
        
        print("\n🎉 All examples completed successfully!")
        print(f"📁 Check the output directory: {Path('./output').absolute()}")
        
    except Exception as e:
        logger.error(f"Application failed: {e}")
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Create output directory
    Path("./output").mkdir(exist_ok=True)
    
    # Run the main application
    exit_code = asyncio.run(main())
    sys.exit(exit_code)