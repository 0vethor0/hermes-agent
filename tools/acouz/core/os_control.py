"""
acouz/core/os_control.py

Ejecución física de acciones del sistema operativo local.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import psutil

from acouz.utils.config import ConfigManager

# Alias habituales → ejecutable (Windows).
_PROGRAM_ALIASES: dict[str, str] = {
    "notepad": "notepad.exe",
    "bloc": "notepad.exe",
    "bloc de notas": "notepad.exe",
    "calculadora": "calc.exe",
    "calc": "calc.exe",
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "explorador": "explorer.exe",
    "explorador de archivos": "explorer.exe",
    "explorer": "explorer.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "cmd": "cmd.exe",
    "terminal": "wt.exe",
    "paint": "mspaint.exe",
    "spotify": "spotify.exe",
    "discord": "discord.exe",
    "vscode": "code.exe",
    "visual studio code": "code.exe",
    "cursor": "cursor.exe",
}


def _normalize_name(name: str) -> str:
    return name.strip().lower()


def _resolve_executable(nombre_programa: str) -> str:
    """Convierte un nombre coloquial en ruta o comando ejecutable."""
    key = _normalize_name(nombre_programa)
    if key in _PROGRAM_ALIASES:
        return _PROGRAM_ALIASES[key]

    # Ya es una ruta absoluta o relativa existente.
    if os.path.isfile(nombre_programa):
        return nombre_programa

    # Nombre con extensión en PATH.
    found = shutil.which(nombre_programa)
    if found:
        return found

    # Probar alias + .exe en Windows.
    if sys.platform == "win32" and not nombre_programa.lower().endswith(".exe"):
        found = shutil.which(f"{nombre_programa}.exe")
        if found:
            return found

    return nombre_programa


def _default_files_dir() -> Path:
    custom = ConfigManager.get("OS_CONTROL_FILES_DIR", "").strip()
    if custom:
        return Path(custom).expanduser()
    return Path.home() / "Desktop"


def _safe_filename(nombre_archivo: str) -> str:
    name = nombre_archivo.strip()
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    if not name:
        raise ValueError("El nombre del archivo no puede estar vacío")
    return name


def abrir_programa(nombre_programa: str) -> dict:
    """Abre un programa por nombre, alias o ruta."""
    if not nombre_programa or not nombre_programa.strip():
        return {"ok": False, "error": "No se indicó ningún programa"}

    target = _resolve_executable(nombre_programa)

    try:
        if sys.platform == "win32":
            os.startfile(target)  # type: ignore[attr-defined]
        else:
            subprocess.Popen([target], start_new_session=True)
        return {"ok": True, "programa": nombre_programa, "ejecutable": target}
    except OSError:
        try:
            subprocess.Popen(target, shell=True)
            return {"ok": True, "programa": nombre_programa, "ejecutable": target}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}


def cerrar_programa(nombre_programa: str) -> dict:
    """Cierra procesos cuyo nombre coincide con el programa indicado."""
    if not nombre_programa or not nombre_programa.strip():
        return {"ok": False, "error": "No se indicó ningún programa"}

    needle = _normalize_name(nombre_programa)
    executable = _resolve_executable(nombre_programa)
    proc_name = Path(executable).name.lower()

    closed: list[str] = []
    errors: list[str] = []

    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = (proc.info.get("name") or "").lower()
            if needle in name or proc_name in name or name.startswith(needle):
                proc.terminate()
                closed.append(name)
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            errors.append(str(exc))

    if closed:
        return {"ok": True, "cerrados": closed, "errores": errors}

    return {
        "ok": False,
        "error": f"No encontré ningún proceso llamado «{nombre_programa}»",
    }


def crear_archivo(nombre_archivo: str, contenido: str = "") -> dict:
    """Crea un archivo de texto en el escritorio (o carpeta configurada)."""
    try:
        safe_name = _safe_filename(nombre_archivo)
        dest_dir = _default_files_dir()
        dest_dir.mkdir(parents=True, exist_ok=True)
        path = dest_dir / safe_name
        path.write_text(contenido or "", encoding="utf-8")
        return {"ok": True, "ruta": str(path)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
