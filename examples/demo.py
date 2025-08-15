#!/usr/bin/env python3
"""
Faceless Video AI - Comprehensive Demo Script

This script demonstrates all the major features and capabilities of the
Faceless Video AI system with practical examples.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import List

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from faceless_video_ai import FacelessVideoAI
from faceless_video_ai.config import Config


def setup_logging():
    """Setup logging for the demo."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"🎬 {title}")
    print("=" * 70)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n📋 {title}")
    print("-" * 50)


async def demo_basic_generation(fvai: FacelessVideoAI):
    """Demonstrate basic video generation from topic."""
    print_section("Basic Video Generation")
    
    print("🚀 Generating a video about 'Machine Learning'...")
    
    try:
        video_path = await fvai.generate_video_from_topic(
            topic="Machine Learning",
            duration=45,
            style="educational",
            target_audience="beginners",
            tone="informative",
            output_path="./output/demo_ml_basic.mp4"
        )
        
        print(f"✅ Basic video generated successfully!")
        print(f"📁 Output: {video_path}")
        print(f"📊 File size: {video_path.stat().st_size / (1024*1024):.1f} MB")
        
        return video_path
        
    except Exception as e:
        print(f"❌ Basic generation failed: {e}")
        return None


async def demo_script_generation(fvai: FacelessVideoAI):
    """Demonstrate video generation from script."""
    print_section("Script-Based Video Generation")
    
    # Read the example script
    script_path = Path("examples/example_script.txt")
    if not script_path.exists():
        print("⚠️  Example script not found, creating a simple one...")
        script = """
        Welcome to our video about Artificial Intelligence!
        
        AI is transforming the world around us in incredible ways.
        From virtual assistants to autonomous vehicles, AI is everywhere.
        
        The future of AI is bright and full of possibilities.
        Thank you for watching!
        """
    else:
        with open(script_path, 'r', encoding='utf-8') as f:
            script = f.read()
    
    print(f"📝 Generating video from script ({len(script)} characters)...")
    
    try:
        video_path = await fvai.generate_video_from_script(
            script=script,
            visual_style="modern",
            output_path="./output/demo_script_video.mp4"
        )
        
        print(f"✅ Script-based video generated successfully!")
        print(f"📁 Output: {video_path}")
        print(f"📊 File size: {video_path.stat().st_size / (1024*1024):.1f} MB")
        
        return video_path
        
    except Exception as e:
        print(f"❌ Script generation failed: {e}")
        return None


async def demo_batch_generation(fvai: FacelessVideoAI):
    """Demonstrate batch video generation."""
    print_section("Batch Video Generation")
    
    # Read topics from file
    topics_path = Path("examples/topics.txt")
    if not topics_path.exists():
        print("⚠️  Topics file not found, using default topics...")
        topics = [
            "Python Programming",
            "Web Development",
            "Data Science"
        ]
    else:
        with open(topics_path, 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip()]
    
    print(f"🔄 Starting batch generation of {len(topics)} videos...")
    print(f"   Topics: {', '.join(topics[:3])}{'...' if len(topics) > 3 else ''}")
    
    try:
        video_paths = await fvai.batch_generate_videos(
            topics=topics[:3],  # Limit to 3 for demo
            duration=30,
            style="educational",
            output_dir="./output/demo_batch"
        )
        
        print(f"✅ Batch generation completed!")
        print(f"📊 Generated {len(video_paths)} videos:")
        
        total_size = 0
        for video_path in video_paths:
            size_mb = video_path.stat().st_size / (1024*1024)
            total_size += size_mb
            print(f"   📁 {video_path.name} ({size_mb:.1f} MB)")
        
        print(f"📊 Total size: {total_size:.1f} MB")
        
        return video_paths
        
    except Exception as e:
        print(f"❌ Batch generation failed: {e}")
        return []


async def demo_custom_configuration():
    """Demonstrate custom configuration options."""
    print_section("Custom Configuration Demo")
    
    print("⚙️  Creating custom configuration...")
    
    try:
        # Create custom config
        config = Config()
        
        # Customize TTS settings
        config.tts.engine = "whisperspeech"
        config.tts.quality = "high"
        config.tts.language = "en"
        
        # Customize video settings
        config.video.resolution = (1280, 720)  # 720p
        config.video.fps = 24
        config.video.use_libopenshot = True
        
        # Customize content settings
        config.content.default_style = "entertainment"
        config.content.include_subtitles = True
        
        # Customize system settings
        config.system.max_concurrent_jobs = 2
        config.system.use_gpu = True
        
        print("✅ Custom configuration created successfully!")
        print(f"   TTS Engine: {config.tts.engine}")
        print(f"   Video Resolution: {config.video.resolution}")
        print(f"   Content Style: {config.content.default_style}")
        print(f"   Max Jobs: {config.system.max_concurrent_jobs}")
        
        # Test with custom config
        print("\n🧪 Testing custom configuration...")
        fvai = FacelessVideoAI(config)
        
        video_path = await fvai.generate_video_from_topic(
            topic="Custom Configuration Test",
            duration=20,
            style="entertainment",
            output_path="./output/demo_custom_config.mp4"
        )
        
        print(f"✅ Custom config test completed!")
        print(f"📁 Output: {video_path}")
        
        return video_path
        
    except Exception as e:
        print(f"❌ Custom configuration demo failed: {e}")
        return None


async def demo_system_status(fvai: FacelessVideoAI):
    """Demonstrate system status and monitoring."""
    print_section("System Status and Monitoring")
    
    try:
        # Get system status
        status = fvai.get_system_status()
        
        print("📊 System Status Overview:")
        print(f"   TTS Engine: {status['tts_engine']['active_engine']}")
        print(f"   Available TTS Engines: {', '.join(status['tts_engine']['available_engines'])}")
        print(f"   Video Resolution: {status['video_resolution']}")
        print(f"   Content Model: {status['content_model']}")
        print(f"   GPU Available: {status['use_gpu']}")
        
        print("\n🔧 Component Status:")
        print(f"   TTS Engine Status: {'✅' if status['tts_engine']['engine_status'] else '❌'}")
        print(f"   Video Composer Status: {'✅' if status['video_composer']['libopenshot_available'] else '❌'}")
        print(f"   Content Generator Status: {'✅' if status['content_generator']['openai_available'] else '❌'}")
        
        print("\n📁 System Paths:")
        print(f"   Temp Directory: {status['system_temp_dir']}")
        print(f"   Output Directory: {status['system_output_dir']}")
        
        return True
        
    except Exception as e:
        print(f"❌ System status demo failed: {e}")
        return False


async def main():
    """Main demo function."""
    print_header("Faceless Video AI - Comprehensive Demo")
    print("This demo showcases all the major features of the Faceless Video AI system.")
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create output directories
        Path("./output").mkdir(exist_ok=True)
        Path("./output/demo_batch").mkdir(exist_ok=True)
        
        # Initialize the system
        print_section("System Initialization")
        print("🚀 Initializing Faceless Video AI system...")
        
        config = Config()
        fvai = FacelessVideoAI(config)
        
        print("✅ System initialized successfully!")
        
        # Run demos
        results = {}
        
        # Demo 1: Basic generation
        results['basic'] = await demo_basic_generation(fvai)
        
        # Demo 2: Script generation
        results['script'] = await demo_script_generation(fvai)
        
        # Demo 3: Batch generation
        results['batch'] = await demo_batch_generation(fvai)
        
        # Demo 4: Custom configuration
        results['custom'] = await demo_custom_configuration()
        
        # Demo 5: System status
        results['status'] = await demo_system_status(fvai)
        
        # Summary
        print_header("Demo Summary")
        
        successful_demos = sum(1 for result in results.values() if result)
        total_demos = len(results)
        
        print(f"📊 Demo Results: {successful_demos}/{total_demos} successful")
        
        if results['basic']:
            print("✅ Basic video generation: Working")
        else:
            print("❌ Basic video generation: Failed")
        
        if results['script']:
            print("✅ Script-based generation: Working")
        else:
            print("❌ Script-based generation: Failed")
        
        if results['batch']:
            print(f"✅ Batch generation: Working ({len(results['batch'])} videos)")
        else:
            print("❌ Batch generation: Failed")
        
        if results['custom']:
            print("✅ Custom configuration: Working")
        else:
            print("❌ Custom configuration: Failed")
        
        if results['status']:
            print("✅ System monitoring: Working")
        else:
            print("❌ System monitoring: Failed")
        
        print(f"\n📁 All generated videos are saved in: {Path('./output').absolute()}")
        print("\n🎉 Demo completed! Check the output directory for generated videos.")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"❌ Demo failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Run the demo
    exit_code = asyncio.run(main())
    sys.exit(exit_code)