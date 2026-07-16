"""
acouz/core/action_handler.py

Orquesta la respuesta de voz y la ejecución en segundo plano de acciones del SO.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import Any, Optional

from acouz.core import os_control
from acouz.core.intent_processor import Intent


def _run_action(accion: str, parametros: dict[str, Any]) -> dict:
    if accion == "abrir_programa":
        nombre = (
            parametros.get("nombre_programa")
            or parametros.get("programa")
            or parametros.get("nombre")
            or ""
        )
        return os_control.abrir_programa(str(nombre))

    if accion == "cerrar_programa":
        nombre = (
            parametros.get("nombre_programa")
            or parametros.get("programa")
            or parametros.get("nombre")
            or ""
        )
        return os_control.cerrar_programa(str(nombre))

    if accion == "crear_archivo":
        nombre = (
            parametros.get("nombre_archivo")
            or parametros.get("archivo")
            or parametros.get("nombre")
            or "documento.txt"
        )
        contenido = parametros.get("contenido") or parametros.get("texto") or ""
        return os_control.crear_archivo(str(nombre), str(contenido))

    return {"ok": False, "error": "Acción desconocida"}


def _default_message(accion: str, parametros: dict[str, Any], result: dict) -> str:
    if not result.get("ok"):
        return result.get("error", "No pude completar la acción")

    if accion == "abrir_programa":
        return f"Listo, abrí {parametros.get('nombre_programa', 'el programa')}."
    if accion == "cerrar_programa":
        return f"Listo, cerré {parametros.get('nombre_programa', 'el programa')}."
    if accion == "crear_archivo":
        ruta = result.get("ruta", parametros.get("nombre_archivo", "el archivo"))
        return f"Archivo creado en {ruta}."
    return "Hecho."


def process_intent(
    intent: Intent,
    speak: Optional[Callable[[str], None]] = None,
    on_complete: Optional[Callable[[dict], None]] = None,
) -> dict:
    """Ejecuta el flujo: hablar confirmación → acción en segundo plano.

    Returns:
        dict con status inicial para herramientas del agente conversacional.
    """
    accion = intent.get("accion", "ninguna")
    parametros = intent.get("parametros") or {}

    if accion == "ninguna":
        return {"status": "skipped", "message": ""}

    respuesta = (intent.get("respuesta_voz") or "").strip()

    def _worker() -> None:
        result = _run_action(accion, parametros)
        if speak and not respuesta and result.get("ok"):
            speak(_default_message(accion, parametros, result))
        if on_complete:
            on_complete(result)

    if speak and respuesta:
        speak(respuesta)

    threading.Thread(target=_worker, daemon=True).start()

    msg = respuesta or _default_message(accion, parametros, {"ok": True})
    return {"status": "ok", "message": msg}


def process_intent_sync(intent: Intent) -> dict:
    """Ejecuta la acción de forma síncrona (para pruebas o herramientas del agente)."""
    accion = intent.get("accion", "ninguna")
    if accion == "ninguna":
        return {"status": "skipped"}

    result = _run_action(accion, intent.get("parametros") or {})
    message = (intent.get("respuesta_voz") or "").strip()
    if not message:
        message = _default_message(accion, intent.get("parametros") or {}, result)

    return {
        "status": "ok" if result.get("ok") else "error",
        "message": message,
        "result": result,
    }
