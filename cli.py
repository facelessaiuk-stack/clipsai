#!/usr/bin/env python3
"""
Command Line Interface for Faceless Video AI

Provides a user-friendly CLI for generating faceless videos with various options.
"""

import asyncio
import click
import logging
import sys
from pathlib import Path
from typing import List, Optional

from faceless_video_ai import FacelessVideoAI
from faceless_video_ai.config import Config


def setup_logging(verbose: bool):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@click.group()
@click.version_option(version="1.0.0", prog_name="Faceless Video AI")
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.pass_context
def cli(ctx, verbose: bool, config: Optional[str]):
    """🎬 Faceless Video AI - Market-Leading Open-Source Video Software
    
    Generate professional faceless videos using AI-powered content generation,
    high-quality TTS, and professional video composition.
    """
    setup_logging(verbose)
    
    # Initialize configuration
    if config:
        ctx.obj = Config(config)
    else:
        ctx.obj = Config()
    
    # Ensure output directory exists
    Path("./output").mkdir(exist_ok=True)


@cli.command()
@click.option('--topic', '-t', required=True, help='Topic for video generation')
@click.option('--duration', '-d', default=60, help='Video duration in seconds')
@click.option('--style', '-s', default='educational', 
              type=click.Choice(['educational', 'entertainment', 'news', 'business', 'tutorial']),
              help='Content style')
@click.option('--audience', '-a', default='general', help='Target audience')
@click.option('--tone', default='informative', 
              type=click.Choice(['formal', 'casual', 'informative', 'entertaining']),
              help='Content tone')
@click.option('--output', '-o', default='./output', help='Output directory')
@click.option('--tts-engine', type=click.Choice(['whisperspeech', 'piper', 'xtts']), 
              help='TTS engine to use')
@click.option('--resolution', default='1920x1080', help='Video resolution (WxH)')
@click.pass_obj
def generate(ctx, topic: str, duration: int, style: str, audience: str, tone: str, 
            output: str, tts_engine: Optional[str], resolution: str):
    """Generate a video from a topic."""
    config = ctx.obj
    
    # Update config with CLI options
    if tts_engine:
        config.tts.engine = tts_engine
    
    if resolution:
        try:
            width, height = resolution.split('x')
            config.video.resolution = (int(width), int(height))
        except ValueError:
            click.echo(f"❌ Invalid resolution format: {resolution}. Use WxH format (e.g., 1920x1080)")
            sys.exit(1)
    
    async def run_generation():
        try:
            fvai = FacelessVideoAI(config)
            
            click.echo(f"🚀 Generating video about '{topic}'...")
            click.echo(f"   Duration: {duration}s")
            click.echo(f"   Style: {style}")
            click.echo(f"   Audience: {audience}")
            click.echo(f"   Tone: {tone}")
            click.echo(f"   TTS Engine: {config.tts.engine}")
            click.echo(f"   Resolution: {config.video.resolution}")
            
            # Generate video
            output_path = Path(output) / f"{topic.replace(' ', '_').lower()}.mp4"
            video_path = await fvai.generate_video_from_topic(
                topic=topic,
                duration=duration,
                style=style,
                target_audience=audience,
                tone=tone,
                output_path=output_path
            )
            
            click.echo(f"✅ Video generated successfully!")
            click.echo(f"📁 Output: {video_path}")
            click.echo(f"📊 File size: {video_path.stat().st_size / (1024*1024):.1f} MB")
            
        except Exception as e:
            click.echo(f"❌ Video generation failed: {e}")
            sys.exit(1)
    
    asyncio.run(run_generation())


@cli.command()
@click.option('--script', '-s', required=True, type=click.Path(exists=True), 
              help='Path to script file')
@click.option('--style', default='modern', 
              type=click.Choice(['modern', 'classic', 'minimal', 'dynamic']),
              help='Visual style')
@click.option('--output', '-o', default='./output', help='Output directory')
@click.option('--resolution', default='1920x1080', help='Video resolution (WxH)')
@click.pass_obj
def script(ctx, script: str, style: str, output: str, resolution: str):
    """Generate a video from an existing script."""
    config = ctx.obj
    
    # Update config with CLI options
    if resolution:
        try:
            width, height = resolution.split('x')
            config.video.resolution = (int(width), int(height))
        except ValueError:
            click.echo(f"❌ Invalid resolution format: {resolution}. Use WxH format (e.g., 1920x1080)")
            sys.exit(1)
    
    async def run_script_generation():
        try:
            fvai = FacelessVideoAI(config)
            
            # Read script file
            script_path = Path(script)
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            click.echo(f"📝 Generating video from script: {script_path.name}")
            click.echo(f"   Style: {style}")
            click.echo(f"   Resolution: {config.video.resolution}")
            click.echo(f"   Script length: {len(script_content)} characters")
            
            # Generate video
            output_path = Path(output) / f"{script_path.stem}_video.mp4"
            video_path = await fvai.generate_video_from_script(
                script=script_content,
                visual_style=style,
                output_path=output_path
            )
            
            click.echo(f"✅ Video generated successfully!")
            click.echo(f"📁 Output: {video_path}")
            click.echo(f"📊 File size: {video_path.stat().st_size / (1024*1024):.1f} MB")
            
        except Exception as e:
            click.echo(f"❌ Video generation failed: {e}")
            sys.exit(1)
    
    asyncio.run(run_script_generation())


@cli.command()
@click.option('--topics', '-t', required=True, type=click.Path(exists=True), 
              help='Path to topics file (one topic per line)')
@click.option('--duration', '-d', default=60, help='Video duration in seconds')
@click.option('--style', '-s', default='educational', 
              type=click.Choice(['educational', 'entertainment', 'news', 'business', 'tutorial']),
              help='Content style')
@click.option('--output', '-o', default='./output/batch', help='Output directory')
@click.option('--max-jobs', default=4, help='Maximum concurrent jobs')
@click.pass_obj
def batch(ctx, topics: str, duration: int, style: str, output: str, max_jobs: int):
    """Generate multiple videos in batch."""
    config = ctx.obj
    
    # Update config
    config.system.max_concurrent_jobs = max_jobs
    
    async def run_batch_generation():
        try:
            fvai = FacelessVideoAI(config)
            
            # Read topics file
            topics_path = Path(topics)
            with open(topics_path, 'r', encoding='utf-8') as f:
                topic_list = [line.strip() for line in f if line.strip()]
            
            click.echo(f"🔄 Starting batch generation of {len(topic_list)} videos...")
            click.echo(f"   Duration: {duration}s")
            click.echo(f"   Style: {style}")
            click.echo(f"   Max concurrent jobs: {max_jobs}")
            click.echo(f"   Output directory: {output}")
            
            # Generate videos
            video_paths = await fvai.batch_generate_videos(
                topics=topic_list,
                duration=duration,
                style=style,
                output_dir=output
            )
            
            click.echo(f"✅ Batch generation completed!")
            click.echo(f"📊 Generated {len(video_paths)} videos:")
            
            total_size = 0
            for video_path in video_paths:
                size_mb = video_path.stat().st_size / (1024*1024)
                total_size += size_mb
                click.echo(f"   📁 {video_path.name} ({size_mb:.1f} MB)")
            
            click.echo(f"📊 Total size: {total_size:.1f} MB")
            
        except Exception as e:
            click.echo(f"❌ Batch generation failed: {e}")
            sys.exit(1)
    
    asyncio.run(run_batch_generation())


@cli.command()
@click.pass_obj
def status(ctx):
    """Show system status and configuration."""
    config = ctx.obj
    
    click.echo("📊 Faceless Video AI System Status")
    click.echo("=" * 50)
    
    # System status
    click.echo(f"🎯 TTS Engine: {config.tts.engine}")
    click.echo(f"🎬 Video Resolution: {config.video.resolution}")
    click.echo(f"🎨 Content Style: {config.content.default_style}")
    click.echo(f"⚡ Max Concurrent Jobs: {config.system.max_concurrent_jobs}")
    click.echo(f"🖥️  GPU Available: {config.system.use_gpu}")
    
    # Check component availability
    click.echo("\n🔧 Component Status:")
    
    try:
        fvai = FacelessVideoAI(config)
        status = fvai.get_system_status()
        
        click.echo(f"   TTS: {'✅' if status['tts_engine']['engine_status'] else '❌'}")
        click.echo(f"   Video: {'✅' if status['video_composer']['libopenshot_available'] else '❌'}")
        click.echo(f"   Content: {'✅' if status['content_generator']['openai_available'] else '❌'}")
        
    except Exception as e:
        click.echo(f"   ❌ System initialization failed: {e}")
    
    # Configuration paths
    click.echo(f"\n📁 Paths:")
    click.echo(f"   Temp Directory: {config.system.temp_dir}")
    click.echo(f"   Output Directory: {config.system.output_dir}")
    click.echo(f"   Cache Directory: {config.system.cache_dir}")


@cli.command()
@click.option('--output', '-o', default='./config.yaml', help='Output configuration file path')
@click.pass_obj
def config_gen(ctx, output: str):
    """Generate a configuration file template."""
    config = ctx.obj
    
    try:
        config.save_to_file(output)
        click.echo(f"✅ Configuration template saved to: {output}")
        click.echo("📝 Edit the file to customize your settings")
    except Exception as e:
        click.echo(f"❌ Failed to save configuration: {e}")


@cli.command()
@click.option('--topic', '-t', required=True, help='Topic to test')
@click.option('--duration', '-d', default=30, help='Test duration in seconds')
@click.pass_obj
def test(ctx, topic: str, duration: int):
    """Test the system with a short video generation."""
    config = ctx.obj
    
    async def run_test():
        try:
            fvai = FacelessVideoAI(config)
            
            click.echo(f"🧪 Testing system with topic: '{topic}'")
            click.echo(f"   Duration: {duration}s")
            click.echo("   This will test all components...")
            
            # Generate test video
            output_path = Path("./output") / f"test_{topic.replace(' ', '_').lower()}.mp4"
            video_path = await fvai.generate_video_from_topic(
                topic=topic,
                duration=duration,
                style="educational",
                output_path=output_path
            )
            
            click.echo(f"✅ Test completed successfully!")
            click.echo(f"📁 Test video: {video_path}")
            
        except Exception as e:
            click.echo(f"❌ Test failed: {e}")
            sys.exit(1)
    
    asyncio.run(run_test())


if __name__ == '__main__':
    cli()