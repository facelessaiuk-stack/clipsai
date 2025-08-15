# standard library imports
from __future__ import annotations
import logging
from typing import Optional

# local imports
from .base import TTSBackend, TTSResult


class Pyttsx3TTSBackend(TTSBackend):
    """
    Simple local TTS using pyttsx3 (open-source). On Linux this uses eSpeak or
    another available engine. This backend is a fallback that does not require
    cloud access and should run entirely offline.
    """

    def synthesize(
        self,
        text: str,
        output_wav_path: str,
        voice: Optional[str] = None,
        sample_rate_hz: int = 22050,
    ) -> TTSResult:
        try:
            import pyttsx3  # type: ignore
        except Exception as import_error:
            logging.error(
                "pyttsx3 is not installed. Install with: pip install 'pyttsx3' or pip install 'clipsai[tts]'"
            )
            raise import_error

        engine = pyttsx3.init()

        # Optionally set voice
        if voice is not None:
            try:
                voices = engine.getProperty("voices")
                matched_voice_id = None
                for v in voices:
                    if voice.lower() in (str(v.id).lower() + " " + str(v.name).lower()):
                        matched_voice_id = v.id
                        break
                if matched_voice_id is not None:
                    engine.setProperty("voice", matched_voice_id)
                else:
                    logging.warning("Requested voice '%s' not found. Using default.", voice)
            except Exception as voice_error:
                logging.warning("Could not set voice due to: %s", voice_error)

        # Note: Not all engines respect sample rate; we save to WAV and accept engine defaults.
        engine.save_to_file(text, output_wav_path)
        engine.runAndWait()

        return TTSResult(audio_path=output_wav_path, sample_rate_hz=sample_rate_hz)