# standard library imports
from __future__ import annotations
import logging
import math
import os
from typing import List, Optional, Tuple

# local imports
from clipsai.media.audio_file import AudioFile
from clipsai.media.video_file import VideoFile
from clipsai.media.editor import MediaEditor
from clipsai.filesys.manager import FileSystemManager
from clipsai.filesys.file import File

from .tts.base import TTSBackend, TTSResult
from .tts.pyttsx3_backend import Pyttsx3TTSBackend
from .composer.slideshow import create_slideshow_from_images


class FacelessVideoGenerator:
    """
    High-level API to generate faceless videos using open-source components.

    This default implementation:
      - synthesizes narration via a local TTS backend (default: pyttsx3)
      - creates a background slideshow (or a solid color) that matches audio length
      - merges narration audio with the composed video using ffmpeg
    """

    def __init__(
        self,
        tts_backend: Optional[TTSBackend] = None,
        resolution: Tuple[int, int] = (1080, 1920),
        fps: int = 30,
    ) -> None:
        if tts_backend is None:
            tts_backend = Pyttsx3TTSBackend()
        self._tts_backend = tts_backend
        self._resolution = resolution
        self._fps = fps
        self._editor = MediaEditor()
        self._fsm = FileSystemManager()

    def generate(
        self,
        script_text: str,
        output_video_path: str,
        image_paths: Optional[List[str]] = None,
        voice: Optional[str] = None,
        sample_rate_hz: int = 22050,
        overwrite: bool = True,
    ) -> str:
        """
        Generate a faceless video.

        Parameters
        ----------
        script_text: str
            Narration text to synthesize.
        output_video_path: str
            Absolute path to final MP4 output.
        image_paths: Optional[List[str]]
            Optional list of background image paths to create a slideshow.
            If omitted, a single-color background is created.
        voice: Optional[str]
            TTS backend voice identifier.
        sample_rate_hz: int
            Audio output sample rate for synthesis (if supported by backend).
        overwrite: bool
            Overwrite existing outputs.

        Returns
        -------
        str
            Path to the generated MP4 video.
        """
        if not isinstance(script_text, str) or len(script_text.strip()) == 0:
            raise ValueError("script_text must be a non-empty string")

        # Prepare filesystem
        output_dir = os.path.dirname(output_video_path)
        if overwrite:
            self._fsm.assert_parent_dir_exists(File(output_video_path))
        else:
            self._fsm.assert_valid_path_for_new_fs_object(output_video_path)

        # 1) TTS synthesis
        temp_audio_path = os.path.join(output_dir, "_faceless_tts.wav")
        tts_result: TTSResult = self._tts_backend.synthesize(
            text=script_text,
            output_wav_path=temp_audio_path,
            voice=voice,
            sample_rate_hz=sample_rate_hz,
        )
        audio_file = AudioFile(tts_result.audio_path)
        audio_file.assert_exists()
        audio_duration = audio_file.get_duration()
        if audio_duration <= 0:
            raise RuntimeError("Synthesized audio has non-positive duration")

        # 2) Compose silent background video
        temp_silent_video_path = os.path.join(output_dir, "_faceless_bg.mp4")
        if image_paths and len(image_paths) > 0:
            per_image = audio_duration / len(image_paths)
            durations = [per_image for _ in image_paths]
            # Adjust the last image duration to match precisely
            durations[-1] += audio_duration - sum(durations)
            slideshow = create_slideshow_from_images(
                image_paths=image_paths,
                durations=durations,
                resolution=self._resolution,
                fps=self._fps,
                output_silent_video_path=temp_silent_video_path,
                overwrite=True,
            )
            if slideshow is None:
                raise RuntimeError("Failed to create slideshow video from images")
            video_bg = slideshow
        else:
            # Single color background using lavfi color source
            width, height = self._resolution
            cmd = [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                f"color=c=black:s={width}x{height}:r={self._fps}",
                "-t",
                str(audio_duration),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                temp_silent_video_path,
            ]
            logging.debug("ffmpeg color bg cmd: %s", cmd)
            import subprocess

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(
                    f"Failed to create background video: {result.returncode}: {result.stderr}"
                )
            video_bg = VideoFile(temp_silent_video_path)
            video_bg.assert_exists()

        # Sanity: trim/pad video length to match audio if needed
        # If background video is shorter/longer than audio by > 0.1s, trim or copy
        bg_duration = video_bg.get_duration()
        if abs(bg_duration - audio_duration) > 0.1:
            # Trim or extend by copying last frame isn't trivial; just trim to audio duration
            trimmed_path = os.path.join(output_dir, "_faceless_bg_trim.mp4")
            trimmed = self._editor.trim(
                media_file=video_bg,
                start_time=0.0,
                end_time=audio_duration,
                trimmed_media_file_path=trimmed_path,
                overwrite=True,
                video_codec="libx264",
                audio_codec="aac",
                crf="18",
                preset="medium",
                num_threads="0",
            )
            if trimmed is not None:
                video_bg = trimmed

        # 3) Merge audio and video
        merged = self._editor.merge_audio_and_video(
            video_file=video_bg,
            audio_file=audio_file,
            merged_video_file_path=output_video_path,
            overwrite=overwrite,
            video_codec="libx264",
            audio_codec="aac",
        )
        if merged is None:
            raise RuntimeError("Merging audio narration with video background failed")

        # Cleanup temp files (best-effort)
        try:
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            if os.path.exists(temp_silent_video_path):
                os.remove(temp_silent_video_path)
            trim_path = os.path.join(output_dir, "_faceless_bg_trim.mp4")
            if os.path.exists(trim_path):
                os.remove(trim_path)
        except Exception:
            pass

        return output_video_path