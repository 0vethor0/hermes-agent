"""
acouz/core/tts_notifier.py

Reproduce notificaciones de voz cortas vía ElevenLabs TTS.
Se usa para avisos del dictado: "Grabando", "Texto listo", etc.
"""

from __future__ import annotations

import io
import threading
from typing import Optional

import sounddevice as sd
import soundfile as sf

from acouz.utils.config import ConfigManager

# Voz premade de respaldo (plan gratuito). George — multilingüe.
_DEFAULT_FREE_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"


class TTSNotifier:
    """Reproduce fragmentos de audio TTS en un hilo demonio."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._resolved_voice_id: Optional[str] = None
        self._voice_warning_shown = False

    def speak(self, text: str) -> None:
        """Convierte *text* a voz y lo reproduce sin bloquear el hilo principal."""
        threading.Thread(target=self._play, args=(text,), daemon=True).start()

    def _resolve_voice_id(self, client) -> str:
        """Elige una voz usable con el plan actual (gratuito → solo premade)."""
        if self._resolved_voice_id:
            return self._resolved_voice_id

        configured = ConfigManager.get("ELEVENLABS_VOICE_ID", "").strip()
        voices = list(client.voices.search().voices)
        by_id = {v.voice_id: v for v in voices}

        if configured and configured in by_id:
            category = getattr(by_id[configured], "category", "") or ""
            if category in ("premade", "cloned", "generated"):
                self._resolved_voice_id = configured
                return configured
            self._warn_once(
                f"La voz configurada ({by_id[configured].name}) requiere plan de pago. "
                "Usando una voz gratuita."
            )

        for voice in voices:
            if getattr(voice, "category", "") == "premade":
                self._resolved_voice_id = voice.voice_id
                if configured and configured != voice.voice_id:
                    self._warn_once(
                        f"Usando voz gratuita «{voice.name}» ({voice.voice_id}). "
                        "Cambia ELEVENLABS_VOICE_ID en Ajustes si quieres otra premade."
                    )
                return voice.voice_id

        self._resolved_voice_id = _DEFAULT_FREE_VOICE_ID
        return _DEFAULT_FREE_VOICE_ID

    def _warn_once(self, message: str) -> None:
        if not self._voice_warning_shown:
            print(f"[TTSNotifier] {message}")
            self._voice_warning_shown = True

    def _format_error(self, exc: Exception) -> str:
        text = str(exc)
        if "paid_plan_required" in text or "status_code: 402" in text:
            return (
                "Tu plan gratuito no puede usar voces de la biblioteca. "
                "Usa una voz «premade» o actualiza tu suscripción en elevenlabs.io."
            )
        if "status_code:" in text and "body:" in text:
            return text.split("body:", 1)[-1].strip()[:200]
        return text

    def _play(self, text: str) -> None:
        api_key = ConfigManager.get("ELEVENLABS_API_KEY")
        model_id = ConfigManager.get("ELEVENLABS_TTS_MODEL", "eleven_flash_v2_5")

        if not api_key:
            return

        try:
            from elevenlabs.client import ElevenLabs  # noqa: PLC0415

            client = ElevenLabs(api_key=api_key)
            voice_id = self._resolve_voice_id(client)

            audio_bytes = b"".join(
                client.text_to_speech.convert(
                    text=text,
                    voice_id=voice_id,
                    model_id=model_id,
                    output_format="mp3_44100_128",
                )
            )
            with io.BytesIO(audio_bytes) as buf:
                data, samplerate = sf.read(buf, dtype="float32")
            with self._lock:
                sd.play(data, samplerate)
                sd.wait()
        except Exception as exc:
            if "paid_plan_required" in str(exc) or "status_code: 402" in str(exc):
                self._resolved_voice_id = None
            print(f"[TTSNotifier] Error: {self._format_error(exc)}")
