"""
acouz/core/os_agent.py

Agente de control del sistema operativo impulsado por Groq.

Flujo por turno:
  1. Escucha micrófono (detección de silencio)
  2. Groq Whisper → texto
  3. Groq LLM → JSON de intención
  4. Ejecuta acción OS + TTS de confirmación (ElevenLabs opcional)
"""

from __future__ import annotations

import io
import threading
import time
from collections.abc import Callable
from typing import Optional

import numpy as np
import sounddevice as sd
from groq import Groq
from PySide6.QtCore import QObject, Signal
from scipy.io import wavfile

from acouz.core.action_handler import process_intent
from acouz.core.intent_processor import extract_intent
from acouz.utils.config import ConfigManager
from acouz.utils.i18n import tr

_SAMPLE_RATE = 16_000
_BLOCK = 320
_SILENCE_RMS = 0.012
_SILENCE_BLOCKS = 60   # ~1.2 s sin voz → fin de turno
_MAX_BLOCKS = 800      # ~16 s máximo por turno
_STOP_WORDS = frozenset({
    "detente", "para", "salir", "apágate", "apagate", "cierra el agente",
    "desactiva el agente", "stop", "cancela",
})


class GroqOSAgent(QObject):
    """Agente OS: escucha → Groq STT → Groq LLM → ejecuta."""

    status_changed = Signal(str)
    action_executed = Signal(str)
    session_started = Signal()
    session_ended = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._speak: Optional[Callable[[str], None]] = None

    @property
    def is_running(self) -> bool:
        return self._running

    def set_speak_callback(self, callback: Callable[[str], None]) -> None:
        self._speak = callback

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False

    # ------------------------------------------------------------------

    def _run(self) -> None:
        api_key = ConfigManager.get("GROQ_API_KEY", "")
        if not api_key:
            self.status_changed.emit(tr("engine.error.nokey"))
            self._running = False
            return
        if not api_key.startswith("gsk_"):
            self.status_changed.emit(tr("engine.error.badkey"))
            self._running = False
            return

        client = Groq(api_key=api_key)
        self.session_started.emit()
        self.status_changed.emit(tr("agent.listening"))

        try:
            while self._running:
                audio = self._record_turn()
                if not self._running:
                    break
                if audio.size < _SAMPLE_RATE // 2:
                    continue

                self.status_changed.emit(tr("engine.processing"))
                text = self._transcribe(client, audio)
                if not text:
                    continue

                self.status_changed.emit(f"Tú: {text[:80]}")
                if self._should_stop(text):
                    break

                intent = extract_intent(text, client)
                accion = intent.get("accion", "ninguna")

                if accion != "ninguna" and ConfigManager.get("OS_CONTROL_ENABLED", "true") == "true":
                    done = threading.Event()

                    def _on_complete(result: dict) -> None:
                        if result.get("ok"):
                            self.action_executed.emit(str(result))
                        else:
                            err = result.get("error", "Error")
                            self.status_changed.emit(f"Acción: {err}")
                            if self._speak:
                                self._speak(err)
                        done.set()

                    process_intent(intent, speak=self._speak, on_complete=_on_complete)
                    done.wait(timeout=30)
                else:
                    reply = intent.get("respuesta_voz") or self._chat_reply(client, text)
                    if reply and self._speak:
                        self._speak(reply)
                    elif reply:
                        self.status_changed.emit(f"Agente: {reply[:80]}")

                if self._running:
                    self.status_changed.emit(tr("agent.listening"))
                    time.sleep(0.3)

        except Exception as exc:
            self.status_changed.emit(f"Agente: {exc}")
        finally:
            self._running = False
            self.session_ended.emit()

    def _resolve_mic(self) -> Optional[int]:
        mic_name = ConfigManager.get("MICROPHONE", "System Default")
        if mic_name == "System Default" or not mic_name:
            return None
        for i, dev in enumerate(sd.query_devices()):
            if dev["name"] == mic_name:
                return i
        return None

    def _record_turn(self) -> np.ndarray:
        """Graba hasta silencio tras detectar voz."""
        chunks: list[np.ndarray] = []
        speech_started = False
        silent_count = 0
        device = self._resolve_mic()

        with sd.InputStream(
            samplerate=_SAMPLE_RATE,
            channels=1,
            dtype="int16",
            blocksize=_BLOCK,
            device=device,
        ) as stream:
            for _ in range(_MAX_BLOCKS):
                if not self._running:
                    break
                data, _ = stream.read(_BLOCK)
                flat = data.flatten()
                rms = float(np.sqrt(np.mean((flat.astype(np.float32) / 32_768.0) ** 2)))

                if rms >= _SILENCE_RMS:
                    speech_started = True
                    silent_count = 0
                    chunks.append(flat.copy())
                elif speech_started:
                    silent_count += 1
                    chunks.append(flat.copy())
                    if silent_count >= _SILENCE_BLOCKS:
                        break

        if not chunks:
            return np.array([], dtype=np.int16)
        return np.concatenate(chunks)

    def _transcribe(self, client: Groq, audio: np.ndarray) -> str:
        wav_io = io.BytesIO()
        wavfile.write(wav_io, _SAMPLE_RATE, audio)
        wav_io.seek(0)
        model = ConfigManager.get("WHISPER_MODEL", "whisper-large-v3-turbo")
        lang = ConfigManager.get("DICTATION_LANGUAGE", "es")
        result = client.audio.transcriptions.create(
            file=("turn.wav", wav_io.read()),
            model=model,
            language=lang,
        )
        return (result.text or "").strip()

    @staticmethod
    def _should_stop(text: str) -> bool:
        lower = text.lower().strip()
        return any(w in lower for w in _STOP_WORDS)

    def _chat_reply(self, client: Groq, text: str) -> str:
        """Respuesta breve cuando no hay acción OS."""
        model = ConfigManager.get("LLM_MODEL", "llama-3.3-70b-versatile")
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Eres un asistente de escritorio en español. "
                            "Responde en una o dos frases cortas. "
                            "Si piden abrir/cerrar programas o crear archivos, "
                            "indica que puedes hacerlo si lo piden claramente."
                        ),
                    },
                    {"role": "user", "content": text},
                ],
                temperature=0.4,
                max_tokens=120,
            )
            return (completion.choices[0].message.content or "").strip()
        except Exception:
            return "No entendí el comando. Prueba: abre la calculadora."
