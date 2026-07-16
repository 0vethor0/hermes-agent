"""
acouz/core/voice_agent.py

Agente conversacional ElevenLabs con herramientas personalizadas.

Flujo:
  VoiceAgent.start()  →  abre sesión WebSocket con ElevenLabs
  El agente escucha, habla y llama herramientas según lo que digas.
  VoiceAgent.stop()   →  cierra la sesión limpiamente.
"""

from __future__ import annotations

import datetime
import threading
from typing import Optional

from PySide6.QtCore import QObject, Signal

from acouz.core.action_handler import process_intent
from acouz.core.intent_processor import intent_from_tool
from acouz.utils.config import ConfigManager


class VoiceAgent(QObject):
    """Encapsula la sesión conversacional de ElevenLabs.

    Signals:
        status_changed (str): Mensaje de estado para la UI.
        command_show_weather (str): Emitido cuando el agente pide mostrar el clima.
        command_activate_dictation (): El agente pide iniciar dictado.
        action_executed (str): Resumen de una acción del SO completada.
        session_started (): Sesión activa.
        session_ended (): Sesión cerrada.
    """

    status_changed = Signal(str)
    command_show_weather = Signal(str)
    command_activate_dictation = Signal()
    action_executed = Signal(str)
    session_started = Signal()
    session_ended = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._conversation = None
        self._thread: Optional[threading.Thread] = None
        self._running = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Inicia la sesión conversacional en un hilo demonio."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Cierra la sesión limpiamente."""
        self._running = False
        if self._conversation:
            try:
                self._conversation.end_session()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Core
    # ------------------------------------------------------------------

    def _run(self) -> None:
        api_key = ConfigManager.get("ELEVENLABS_API_KEY")
        agent_id = ConfigManager.get("ELEVENLABS_AGENT_ID")

        if not api_key or not agent_id:
            self.status_changed.emit("ElevenLabs: falta API key o Agent ID")
            return

        try:
            from elevenlabs.client import ElevenLabs                               # noqa
            from elevenlabs.conversational_ai.conversation import Conversation   # noqa
            from elevenlabs.conversational_ai.default_audio_interface import (      # noqa
                DefaultAudioInterface,
            )

            client = ElevenLabs(api_key=api_key)
            client_tools = self._build_tools()

            self._conversation = Conversation(
                client=client,
                agent_id=agent_id,
                requires_auth=True,
                audio_interface=DefaultAudioInterface(),
                client_tools=client_tools,
                callback_agent_response=self._on_agent_response,
                callback_user_transcript=self._on_user_transcript,
            )

            self.session_started.emit()
            self.status_changed.emit("Agente activo")
            self._conversation.start_session()
            self._conversation.wait_for_session_end()

        except Exception as exc:
            self.status_changed.emit(f"Agente: error — {exc}")
        finally:
            self._running = False
            self.session_ended.emit()

    # ------------------------------------------------------------------
    # Callbacks de la conversación
    # ------------------------------------------------------------------

    def _on_agent_response(self, response: str) -> None:
        self.status_changed.emit(f"Agente: {response[:60]}…")

    def _on_user_transcript(self, transcript: str) -> None:
        self.status_changed.emit(f"Tú: {transcript[:60]}")

    # ------------------------------------------------------------------
    # Herramientas que el agente puede invocar
    # ------------------------------------------------------------------

    def _dispatch_tool(self, accion: str, params: dict) -> dict:
        """Puente común para herramientas ElevenLabs → action_handler."""
        nombre = (
            params.get("nombre_programa")
            or params.get("nombre_archivo")
            or params.get("programa")
            or params.get("archivo")
            or ""
        )
        respuesta = params.get("respuesta_voz", "")
        if not respuesta:
            if accion == "abrir_programa":
                respuesta = f"Abriendo {nombre}."
            elif accion == "cerrar_programa":
                respuesta = f"Cerrando {nombre}."
            elif accion == "crear_archivo":
                respuesta = f"Creando {params.get('nombre_archivo', 'el archivo')}."

        intent = intent_from_tool(accion, params, respuesta)

        def _on_complete(result: dict) -> None:
            if result.get("ok"):
                self.action_executed.emit(str(result))
            else:
                self.status_changed.emit(f"Acción: {result.get('error', 'error')}")

        return process_intent(intent, speak=None, on_complete=_on_complete)

    def _build_tools(self):
        """Registra las herramientas cliente disponibles para el agente."""
        from elevenlabs.conversational_ai.conversation import ClientTools  # noqa

        tools = ClientTools()

        def get_current_time(params: dict) -> dict:
            now = datetime.datetime.now()
            return {
                "time": now.strftime("%H:%M"),
                "date": now.strftime("%A %d de %B de %Y"),
            }

        tools.register("get_current_time", get_current_time, is_async=False)

        def show_weather(params: dict) -> dict:
            city = params.get("city", "España")
            self.command_show_weather.emit(city)
            return {"status": "ok", "message": f"Mostrando clima de {city}"}

        tools.register("show_weather", show_weather, is_async=False)

        def activate_dictation(params: dict) -> dict:
            return {
                "status": "info",
                "message": "El dictado usa su propio atajo. Mantén la tecla de dictado para transcribir.",
            }

        tools.register("activate_dictation", activate_dictation, is_async=False)

        # ── Control del sistema operativo ────────────────────────────
        def abrir_programa(params: dict) -> dict:
            return self._dispatch_tool("abrir_programa", params)

        def cerrar_programa(params: dict) -> dict:
            return self._dispatch_tool("cerrar_programa", params)

        def crear_archivo(params: dict) -> dict:
            return self._dispatch_tool("crear_archivo", params)

        tools.register("abrir_programa", abrir_programa, is_async=False)
        tools.register("cerrar_programa", cerrar_programa, is_async=False)
        tools.register("crear_archivo", crear_archivo, is_async=False)

        return tools
