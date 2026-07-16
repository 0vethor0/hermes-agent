"""
acouz/core/intent_processor.py

Extrae intenciones estructuradas (JSON) desde texto del usuario vía Groq.
"""

from __future__ import annotations

import json
import re
from typing import Any, Literal, TypedDict

from groq import Groq

from acouz.utils.config import ConfigManager

Accion = Literal["abrir_programa", "cerrar_programa", "crear_archivo", "ninguna"]


class Intent(TypedDict, total=False):
    accion: Accion
    parametros: dict[str, Any]
    respuesta_voz: str


_SYSTEM_PROMPT = """Eres el cerebro de un agente que controla el PC del usuario (Windows).
Analiza lo que dijo y responde SOLO con JSON válido (sin markdown).

Formato:
{
  "accion": "abrir_programa" | "cerrar_programa" | "crear_archivo" | "ninguna",
  "parametros": { ... },
  "respuesta_voz": "confirmación breve en español"
}

Acciones:
- abrir_programa → {"nombre_programa": "calculadora|chrome|notepad|..."}
- cerrar_programa → {"nombre_programa": "..."}
- crear_archivo → {"nombre_archivo": "x.txt", "contenido": "texto"}
- ninguna → conversación sin acción OS; respuesta_voz = respuesta corta al usuario

Prioriza interpretar órdenes del sistema: abrir, cerrar, crear archivo, lanzar app.
Si es ambiguo pero suena a comando OS, elige la acción más probable.
"""


def _empty_intent() -> Intent:
    return {"accion": "ninguna", "parametros": {}, "respuesta_voz": ""}


def _parse_json_response(raw: str) -> Intent:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    data = json.loads(text)
    accion = data.get("accion", "ninguna")
    if accion not in ("abrir_programa", "cerrar_programa", "crear_archivo", "ninguna"):
        accion = "ninguna"

    return {
        "accion": accion,
        "parametros": data.get("parametros") or {},
        "respuesta_voz": (data.get("respuesta_voz") or "").strip(),
    }


def extract_intent(text: str, client: Groq | None = None) -> Intent:
    """Envía *text* al LLM y devuelve la intención estructurada."""
    if not text or not text.strip():
        return _empty_intent()

    api_key = ConfigManager.get("GROQ_API_KEY")
    if not api_key or not api_key.startswith("gsk_"):
        return _empty_intent()

    groq = client or Groq(api_key=api_key)
    model = ConfigManager.get("LLM_MODEL", "llama-3.3-70b-versatile")

    try:
        completion = groq.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": text.strip()},
            ],
            temperature=0.0,
            max_tokens=512,
            response_format={"type": "json_object"},
        )
        raw = completion.choices[0].message.content or "{}"
        return _parse_json_response(raw)
    except Exception:
        return _empty_intent()


def intent_from_tool(accion: str, parametros: dict, respuesta_voz: str = "") -> Intent:
    """Construye un Intent desde parámetros de herramienta ElevenLabs."""
    valid: Accion = (
        accion
        if accion in ("abrir_programa", "cerrar_programa", "crear_archivo", "ninguna")
        else "ninguna"
    )
    return {
        "accion": valid,
        "parametros": parametros or {},
        "respuesta_voz": respuesta_voz,
    }
