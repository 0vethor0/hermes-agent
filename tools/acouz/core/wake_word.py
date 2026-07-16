"""
acouz/core/wake_word.py

Detecta la palabra de activación usando openWakeWord (100 % offline, sin claves).
Emite la señal `detected` cuando la escucha.
"""

from __future__ import annotations

import threading
from typing import Optional

import numpy as np
from PySide6.QtCore import QObject, Signal

from acouz.core.wake_models import ensure_wake_models
from acouz.utils.config import ConfigManager

# Audio constants for openWakeWord: 16 kHz, 80 ms frames.
_SAMPLE_RATE = 16_000
_FRAME_SAMPLES = 1280          # 80 ms × 16 kHz
_THRESHOLD = 0.5               # default confidence cutoff

# Map of built-in model names → human-readable labels shown in the UI.
BUILTIN_WAKE_WORDS: dict[str, str] = {
    "hey_jarvis":   "Hey Jarvis",
    "alexa":        "Alexa",
    "hey_mycroft":  "Hey Mycroft",
    "hey_rhasspy":  "Hey Rhasspy",
}


def available_wake_words() -> dict[str, str]:
    """Return the map of supported wake-word model keys → display names."""
    return dict(BUILTIN_WAKE_WORDS)


class WakeWordListener(QObject):
    """Background listener that emits `detected` when the wake word is heard."""

    detected = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._running = False
        self._thread: Optional[threading.Thread] = None

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
        wake_key = ConfigManager.get("WAKE_WORD_MODEL", "hey_jarvis")
        threshold = float(ConfigManager.get("WAKE_WORD_THRESHOLD", str(_THRESHOLD)))

        try:
            import openwakeword                        # noqa: PLC0415
            from openwakeword.model import Model       # noqa: PLC0415
            import sounddevice as sd                   # noqa: PLC0415

            ensure_wake_models(wake_key)

            model = Model(
                wakeword_models=[wake_key],
                inference_framework="onnx",
            )

            with sd.InputStream(
                samplerate=_SAMPLE_RATE,
                channels=1,
                dtype="int16",
                blocksize=_FRAME_SAMPLES,
            ) as stream:
                print(f"[WakeWord] Listening for '{wake_key}' …")
                while self._running:
                    audio, _ = stream.read(_FRAME_SAMPLES)
                    pcm = audio.flatten().astype(np.int16)
                    prediction = model.predict(pcm)
                    # prediction → {"model_name": score, ...}
                    for score in prediction.values():
                        if score > threshold:
                            print("[WakeWord] Detected!")
                            self.detected.emit()
                            model.reset()
                            break

        except ImportError:
            print("[WakeWord] openwakeword not installed. Wake word disabled.")
        except Exception as exc:
            print(f"[WakeWord] Error: {exc}")
