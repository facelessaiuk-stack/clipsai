# standard library imports
from __future__ import annotations
import logging
import os
import subprocess
import uuid
from typing import List, Tuple

# local package imports
from clipsai.media.image_file import ImageFile
from clipsai.media.video_file import VideoFile
from clipsai.media.editor import MediaEditor
from clipsai.filesys.manager import FileSystemManager
from clipsai.filesys.file import File


SUCCESS = 0


def _ffmpeg_create_segment_from_image(
    image_path: str,
    duration: float,
    resolution: Tuple[int, int],
    fps: int,
    segment_path: str,
) -> bool:
    width, height = resolution
    vf = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-t",
        str(max(0.01, duration)),
        "-i",
        image_path,
        "-vf",
        vf,
        "-r",
        str(fps),
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        segment_path,
    ]
    logging.debug("ffmpeg image->segment cmd: %s", cmd)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != SUCCESS:
        logging.error(
            "Failed to create segment from image. Return %s, stdout: %s, stderr: %s",
            result.returncode,
            result.stdout,
            result.stderr,
        )
        return False
    return True


def create_slideshow_from_images(
    image_paths: List[str],
    durations: List[float],
    resolution: Tuple[int, int],
    fps: int,
    output_silent_video_path: str,
    overwrite: bool = True,
) -> VideoFile | None:
    """
    Create a silent slideshow video by stitching per-image segments and concatenating.

    Parameters
    ----------
    image_paths: List[str]
        Absolute paths to images.
    durations: List[float]
        Display durations per image in seconds (same length as image_paths).
    resolution: Tuple[int, int]
        Output width, height in pixels.
    fps: int
        Frames per second.
    output_silent_video_path: str
        Absolute path to store resulting silent video.
    overwrite: bool
        Overwrite output if exists.
    """
    assert len(image_paths) == len(durations) and len(image_paths) > 0

    fsm = FileSystemManager()
    if overwrite:
        fsm.assert_parent_dir_exists(File(output_silent_video_path))
    else:
        fsm.assert_valid_path_for_new_fs_object(output_silent_video_path)

    segments: List[VideoFile] = []
    temp_dir = os.path.join(
        os.path.dirname(output_silent_video_path), f".faceless_tmp_{uuid.uuid4().hex}"
    )
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Create a segment for each image
        for idx, (img_path, dur) in enumerate(zip(image_paths, durations)):
            img = ImageFile(img_path)
            img.assert_exists()
            seg_path = os.path.join(temp_dir, f"seg_{idx:04d}.mp4")
            ok = _ffmpeg_create_segment_from_image(
                image_path=img.path,
                duration=dur,
                resolution=resolution,
                fps=fps,
                segment_path=seg_path,
            )
            if not ok:
                return None
            segment = VideoFile(seg_path)
            segment.assert_exists()
            segments.append(segment)

        # If only one segment, just copy/rename
        editor = MediaEditor()
        if len(segments) == 1:
            copied = editor.copy_temporal_media_file(
                media_file=segments[0],
                copied_media_file_path=output_silent_video_path,
                overwrite=overwrite,
                video_codec="libx264",
                audio_codec="aac",
                crf="18",
                preset="medium",
            )
            return copied

        # Concatenate segments
        concatenated = editor.concatenate(
            media_files=segments,
            concatenated_media_file_path=output_silent_video_path,
            overwrite=overwrite,
        )
        return concatenated
    finally:
        # Best-effort cleanup of temp files
        try:
            for fname in os.listdir(temp_dir):
                try:
                    os.remove(os.path.join(temp_dir, fname))
                except Exception:
                    pass
            os.rmdir(temp_dir)
        except Exception:
            pass