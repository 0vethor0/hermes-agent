"""
Descarga de modelos openWakeWord con respaldo en Hugging Face.

En algunas redes (p. ej. routers que bloquean release-assets.githubusercontent.com)
la descarga oficial falla. Hugging Face suele seguir accesible.
"""

from __future__ import annotations

import os
import pathlib
from typing import Iterable
from urllib.request import urlretrieve

import openwakeword

_FEATURE_FILES = ("embedding_model.onnx", "melspectrogram.onnx")

# Modelos de wake word disponibles en Hugging Face cuando GitHub no responde.
_HF_WAKE_ALIASES: dict[str, tuple[str, str, str]] = {
    # repo, archivo remoto, nombre local esperado por openWakeWord
    "hey_jarvis": (
        "Soulcreek2/speechkit-wakeword-models",
        "hey_jarvis.onnx",
        "hey_jarvis_v0.1.onnx",
    ),
}


def _models_dir() -> pathlib.Path:
    return pathlib.Path(openwakeword.__file__).parent / "resources" / "models"


def _hf_url(repo: str, filename: str) -> str:
    return f"https://huggingface.co/{repo}/resolve/main/{filename}"


def _download_hf(url: str, dest: pathlib.Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"[WakeWord] Descargando {dest.name} desde Hugging Face …")
    urlretrieve(url, dest)


def _missing(files: Iterable[str], directory: pathlib.Path) -> list[str]:
    return [name for name in files if not (directory / name).exists()]


def ensure_wake_models(wake_key: str) -> None:
    """Garantiza que los modelos ONNX necesarios estén en disco."""
    target = _models_dir()
    wake_file = f"{wake_key}_v0.1.onnx"
    needed = list(_FEATURE_FILES) + [wake_file]
    if not _missing(needed, target):
        return

    try:
        openwakeword.utils.download_models(model_names=[f"{wake_key}_v0.1"])
        if not _missing(needed, target):
            return
    except Exception as exc:
        print(f"[WakeWord] Descarga desde GitHub falló ({exc}). Probando Hugging Face …")

    # Modelos base compartidos por todos los wake words.
    features_repo = "littlebearlabs/openwakeword-features"
    for filename in _missing(_FEATURE_FILES, target):
        _download_hf(_hf_url(features_repo, filename), target / filename)

    if not (target / wake_file).exists():
        alias = _HF_WAKE_ALIASES.get(wake_key)
        if alias is None:
            raise RuntimeError(
                f"No hay espejo de Hugging Face para '{wake_key}'. "
                "Descarga manual desde https://github.com/dscripka/openWakeWord/releases "
                f"y coloca {wake_file} en {target}"
            )
        repo, remote_name, local_name = alias
        _download_hf(_hf_url(repo, remote_name), target / local_name)

    still_missing = _missing(needed, target)
    if still_missing:
        raise RuntimeError(
            "Faltan modelos de wake word: "
            + ", ".join(still_missing)
            + f". Carpeta esperada: {target}"
        )
