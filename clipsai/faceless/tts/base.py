# standard library imports
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class TTSResult:
    audio_path: str
    sample_rate_hz: int


class TTSBackend(ABC):
    """
    Abstract base interface for text-to-speech backends.
    """

    @abstractmethod
    def synthesize(
        self,
        text: str,
        output_wav_path: str,
        voice: Optional[str] = None,
        sample_rate_hz: int = 22050,
    ) -> TTSResult:
        """
        Synthesize speech from text to a WAV file.

        Parameters
        ----------
        text: str
            Text to synthesize.
        output_wav_path: str
            Absolute path to the output WAV file.
        voice: Optional[str]
            Backend-specific voice identifier/name.
        sample_rate_hz: int
            Desired sample rate in Hz for the output WAV.

        Returns
        -------
        TTSResult
            Information about the synthesized audio.
        """
        raise NotImplementedError