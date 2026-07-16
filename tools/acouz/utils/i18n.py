"""
AcouZ - Open-source AI voice dictation
Copyright (c) 2025-2026 DoodzProg
Licensed under the MIT License

Lightweight three-language (ES / EN / FR) internationalisation module.

All user-visible strings live in :data:`_STRINGS`.  Call :func:`tr` anywhere in
the codebase to get the translation for the current ``UI_LANGUAGE`` setting.
Adding a new language requires only:
  1. Adding the new language code to every entry in ``_STRINGS``.
  2. Adding the combo option in :mod:`~acouz.ui.pages.general`.

Language codes follow ISO 639-1 (``"es"``, ``"en"``, ``"fr"``).
Default language: ``"es"`` (Spanish).
"""

from __future__ import annotations

# ------------------------------------------------------------------
# String table
# ------------------------------------------------------------------

#: ``key -> {lang_code -> translated_string}``
_STRINGS: dict[str, dict[str, str]] = {

    # -- Navigation (sidebar) --
    "nav.home":     {"en": "Home",     "fr": "Accueil", "es": "Inicio"},
    "nav.settings": {"en": "Settings", "fr": "Paramètres", "es": "Configuración"},
    "nav.api":      {"en": "API Groq", "fr": "API Groq", "es": "API Groq"},
    "nav.audio":    {"en": "Audio",    "fr": "Audio", "es": "Audio"},
    "nav.about":    {"en": "About",    "fr": "À propos", "es": "Acerca de"},

    # -- Sidebar misc --
    "sidebar.quit":        {"en": "  Close AcouZ",  "fr": "  Fermer AcouZ", "es": "  Cerrar AcouZ"},
    "sidebar.status.init": {"en": "Initializing…",    "fr": "Initialisation…", "es": "Inicializando…"},

    # -- Home page --
    "home.title":                {"en": "Dashboard",    "fr": "Tableau de bord", "es": "Panel de control"},
    "home.stat.words.label":     {"en": "Words today",  "fr": "Dictés aujourd'hui", "es": "Palabras hoy"},
    "home.stat.time.label":      {"en": "Recording time",  "fr": "Temps de dictée", "es": "Tiempo de grabación"},
    "home.stat.wpm.label":       {"en": "Avg. speed",   "fr": "Vitesse moyenne", "es": "Velocidad promedio"},
    "home.stat.sessions.label":  {"en": "Sessions",     "fr": "Sessions complètes", "es": "Sesiones completas"},
    "home.stat.words.unit":      {"en": "words",        "fr": "mots", "es": "palabras"},
    "home.stat.wpm.unit":        {"en": "WPM",          "fr": "MPM", "es": "PPM"},
    "home.section.shortcuts":    {"en": "Active shortcuts",  "fr": "Raccourcis actifs", "es": "Atajos activos"},
    "home.section.activity":     {"en": "RECENT ACTIVITY",   "fr": "ACTIVITÉ RÉCENTE", "es": "ACTIVIDAD RECIENTE"},
    "home.btn.clear":            {"en": "Reset",              "fr": "Réinitialiser", "es": "Reiniciar"},
    "home.empty":   {
        "en": "No dictation yet — let's get started!",
        "fr": "Aucune dictée pour l'instant — lancez-vous !",
        "es": "¡Aún no hay dictados — comencemos!",
    },
    "home.shortcut.dictate": {"en": "Simple dictation",      "fr": "Dictée simple", "es": "Dictado simple"},
    "home.shortcut.context": {
        "en": "Context instructions",
        "fr": "Instructions avec contexte",
        "es": "Instrucciones con contexto",
    },
    "home.shortcut.hold": {
        "en": "Hold to speak, release to transcribe",
        "fr": "Maintenez pour parler, relâchez pour transcrire",
        "es": "Mantén presionado para hablar, suelta para transcribir",
    },
    "home.shortcut.toggle": {
        "en": "Press to start, press again to transcribe",
        "fr": "Appuyez pour démarrer, ré-appuyez pour transcrire",
        "es": "Presiona para comenzar, presiona de nuevo para transcribir",
    },
    "home.shortcut.agent": {
        "en": "OS control agent",
        "fr": "Agent contrôle OS",
        "es": "Agente control del sistema",
    },
    "home.shortcut.agent.toggle": {
        "en": "Press to start/stop voice agent",
        "fr": "Appuyez pour démarrer/arrêter l'agent vocal",
        "es": "Presiona para iniciar/detener el agente de voz",
    },

    # -- General / Settings page --
    "general.title":             {"en": "Settings",             "fr": "Paramètres", "es": "Configuración"},
    "general.section.hotkeys":   {"en": "Keyboard shortcuts",   "fr": "Raccourci clavier", "es": "Atajos de teclado"},
    "general.hk.desc": {
        "en": "Click a button below, then press your key combination.",
        "fr": "Cliquez sur un bouton ci-dessous, puis appuyez sur votre combinaison.",
        "es": "Haz clic en un botón abajo, luego presiona tu combinación de teclas.",
    },
    "general.hk.dictate":    {"en": "Simple dictation",       "fr": "Dictée simple", "es": "Dictado simple"},
    "general.hk.context":    {
        "en": "Context instructions",
        "fr": "Instructions avec contexte",
        "es": "Instrucciones con contexto",
    },
    "general.hk.agent": {
        "en": "OS control agent (ElevenLabs)",
        "fr": "Agent contrôle OS (ElevenLabs)",
        "es": "Agente control del SO (ElevenLabs)",
    },
    "general.hk.agent.desc": {
        "en": "Toggle voice agent — separate from dictation. Wake word also starts this.",
        "fr": "Active/désactive l'agent vocal — séparé de la dictée.",
        "es": "Activa/desactiva el agente de voz — separado del dictado. La wake word también lo inicia.",
    },
    "general.hk.listening":  {"en": "Press your keys…",       "fr": "Appuyez sur vos touches…", "es": "Presiona tus teclas…"},
    "general.hk.edit":       {"en": "Edit",                   "fr": "Modifier", "es": "Editar"},
    "general.hk.mode":       {"en": "Trigger mode",           "fr": "Mode de déclenchement", "es": "Modo de activación"},
    "general.hk.mode.hold":  {"en": "Hold (Push-to-Talk)",    "fr": "Maintien", "es": "Mantener (Push-to-Talk)"},
    "general.hk.mode.toggle":{"en": "Press (Toggle)",         "fr": "Appui simple", "es": "Presionar (Alternar)"},

    "general.section.behaviour":   {"en": "Behaviour",          "fr": "Comportement", "es": "Comportamiento"},
    "general.startup.label":       {"en": "Launch at startup",   "fr": "Démarrage automatique", "es": "Iniciar al arrancar"},
    "general.startup.desc":        {
        "en": "Start AcouZ when Windows starts",
        "fr": "Lancer AcouZ au démarrage de Windows",
        "es": "Iniciar AcouZ cuando Windows arranca",
    },
    "general.sound.label":         {"en": "Confirmation sound",  "fr": "Son de confirmation", "es": "Sonido de confirmación"},
    "general.sound.desc":          {
        "en": "Play a chime at the start and end of dictation",
        "fr": "Jouer un son au début et à la fin de la dictée",
        "es": "Reproducir un sonido al inicio y final del dictado",
    },
    "general.overlay.label":       {"en": "Dictation overlay",   "fr": "Bulle de dictée", "es": "Indicador de dictado"},
    "general.overlay.desc":        {
        "en": "Show the floating indicator during recording",
        "fr": "Afficher l'indicateur flottant pendant l'enregistrement",
        "es": "Mostrar el indicador flotante durante la grabación",
    },

    "general.section.language":    {"en": "Language & Region",   "fr": "Langue & Région", "es": "Idioma y Región"},
    "general.lang.dictation.label":{"en": "Dictation language",  "fr": "Langue de dictée", "es": "Idioma de dictado"},
    "general.lang.dictation.desc": {
        "en": "Main language used for transcription",
        "fr": "Langue principale utilisée pour la transcription",
        "es": "Idioma principal utilizado para la transcripción",
    },
    "general.lang.ui.label":       {"en": "Interface language",  "fr": "Langue de l'interface", "es": "Idioma de la interfaz"},
    "general.lang.ui.desc":        {
        "en": "AcouZ display language",
        "fr": "Langue d'affichage de AcouZ",
        "es": "Idioma de visualización de AcouZ",
    },

    # -- API page --
    "api.title":   {"en": "Groq API Key",   "fr": "Clé API Groq", "es": "Clave API Groq"},
    "api.banner":  {
        "en": "Your key is stored locally in your user profile.",
        "fr": "Votre clé est stockée localement dans votre profil.",
        "es": "Tu clave se almacena localmente en tu perfil de usuario.",
    },
    "api.section":       {"en": "Configuration",  "fr": "Configuration", "es": "Configuración"},
    "api.key.label":     {"en": "Groq API Key",   "fr": "Clé API Groq", "es": "Clave API Groq"},
    "api.get.free.key":  {"en": "Get a free API key →", "fr": "Obtenir une clé gratuite →", "es": "Obtener una clave API gratuita →"},
    "api.btn.verify":    {"en": "Verify key",     "fr": "Vérifier la clé", "es": "Verificar clave"},
    "api.btn.save":      {"en": "Save",           "fr": "Sauvegarder", "es": "Guardar"},
    "api.verify.empty":    {"en": "Key is empty!",  "fr": "Clé vide !", "es": "¡La clave está vacía!"},
    "api.verify.checking": {"en": "Checking…",      "fr": "Vérification…", "es": "Verificando…"},
    "api.verify.valid":    {"en": "Key is valid!",  "fr": "Clé valide !", "es": "¡La clave es válida!"},
    "api.verify.invalid":  {"en": "Invalid key",    "fr": "Clé invalide", "es": "Clave inválida"},
    "api.verify.error.title": {
        "en": "Verification error",
        "fr": "Erreur de vérification",
        "es": "Error de verificación",
    },
    "api.verify.error.msg": {
        "en": "The API key was rejected by Groq.\n\nDetails: {exc}",
        "fr": "La clé API a été rejetée par Groq.\n\nDétail : {exc}",
        "es": "La clave API fue rechazada por Groq.\n\nDetalles: {exc}",
    },
    "api.save.done": {"en": "Saved!", "fr": "Sauvegardé !", "es": "¡Guardado!"},

    # -- Audio page --
    "audio.title":          {"en": "Audio",               "fr": "Audio", "es": "Audio"},
    "audio.section.input":  {"en": "Input device",        "fr": "Périphérique d'entrée", "es": "Dispositivo de entrada"},
    "audio.mic.label":      {"en": "Microphone",          "fr": "Microphone", "es": "Micrófono"},
    "audio.mic.desc":       {
        "en": "Audio source used for dictation",
        "fr": "Source audio utilisée pour la dictée",
        "es": "Fuente de audio utilizada para el dictado",
    },
    "audio.mic.none":       {
        "en": "No microphone detected",
        "fr": "Aucun microphone détecté",
        "es": "No se detectó ningún micrófono",
    },
    "audio.test.label":     {"en": "Audio Test",          "fr": "Test Audio", "es": "Prueba de Audio"},
    "audio.test.desc":      {
        "en": "Hear your voice with a short delay (0.5 s)",
        "fr": "Écoutez votre retour vocal avec un léger décalage (0.5 s)",
        "es": "Escucha tu voz con un breve retraso (0.5 s)",
    },
    "audio.test.start":     {"en": "Test microphone",     "fr": "Tester le micro", "es": "Probar micrófono"},
    "audio.test.stop":      {
        "en": "Stop test",
        "fr": "Arrêter",
        "es": "Detener prueba",
    },

    # -- About page --
    "about.tagline": {
        "en": "Open-source voice dictation. Fast, private, free.",
        "fr": "Dictée vocale open-source. Rapide, privée, gratuite.",
        "es": "Dictado de voz de código abierto. Rápido, privado, gratuito.",
    },
    "about.section.version":  {"en": "Version",      "fr": "Version", "es": "Versión"},
    "about.version.label":    {"en": "Current version", "fr": "Version actuelle", "es": "Versión actual"},
    "about.version.desc":     {
        "en": "Phase 4 — GUI & .exe",
        "fr": "Phase 4 — Interface graphique & .exe",
        "es": "Fase 4 — Interfaz gráfica & .exe",
    },
    "about.env.label":        {"en": "Environment",  "fr": "Environnement", "es": "Entorno"},
    "about.env.desc":         {
        "en": "Groq Whisper transcription engine",
        "fr": "Moteur de transcription Groq Whisper",
        "es": "Motor de transcripción Groq Whisper",
    },
    "about.section.links":    {"en": "Links",         "fr": "Liens", "es": "Enlaces"},
    "about.link.github":      {
        "en": "GitHub — Source code & releases",
        "fr": "GitHub — Code source et releases",
        "es": "GitHub — Código fuente y lanzamientos",
    },
    "about.link.bug":         {"en": "Report a bug",         "fr": "Signaler un bug", "es": "Reportar un error"},
    "about.link.feature":     {"en": "Request a feature",    "fr": "Proposer une fonctionnalité", "es": "Solicitar una función"},
    "about.btn.update":       {"en": "Check for updates",    "fr": "Vérifier les mises à jour", "es": "Buscar actualizaciones"},
    "about.update.checking":  {"en": "Checking…",            "fr": "Vérification…", "es": "Verificando…"},
    "about.update.available": {
        "en": "Update available: v{tag}",
        "fr": "Mise à jour disponible : v{tag}",
        "es": "Actualización disponible: v{tag}",
    },
    "about.update.uptodate":  {"en": "You are up to date.",   "fr": "Vous êtes à jour.", "es": "Estás actualizado."},
    "about.update.noreleases":{"en": "No releases found yet.", "fr": "Aucune release disponible.", "es": "No se encontraron lanzamientos aún."},
    "about.update.error":     {"en": "Error {code}.",          "fr": "Erreur {code}.", "es": "Error {code}."},
    "about.update.unreachable":{
        "en": "Could not reach GitHub.",
        "fr": "Impossible de contacter GitHub.",
        "es": "No se pudo contactar con GitHub.",
    },

    # -- Voice overlay labels --
    "overlay.dictation":   {"en": "Dictation…", "fr": "Dictée…", "es": "Dictando…"},
    "overlay.context":     {"en": "Instructions…", "fr": "Instructions…", "es": "Instrucciones…"},

    # -- Engine status messages --
    "engine.recording":    {"en": "Recording…",           "fr": "Enregistrement…", "es": "Grabando…"},
    "engine.processing":   {"en": "Processing…",          "fr": "Traitement…", "es": "Procesando…"},
    "engine.cleaning":     {"en": "Cleaning up (LLM)…",   "fr": "Nettoyage (LLM)…", "es": "Limpiando (LLM)…"},
    "engine.ready":        {"en": "Ready to dictate",     "fr": "Prêt à dicter", "es": "Listo para dictar"},
    "engine.error":        {"en": "Error",                "fr": "Erreur", "es": "Error"},
    "engine.error.conn":   {"en": "Connection error",     "fr": "Erreur de connexion", "es": "Error de conexión"},
    "engine.error.nokey":  {
        "en": "API key missing. Go to the API Groq tab.",
        "fr": "Clé API manquante. Allez dans l'onglet API Groq.",
        "es": "Falta la clave API. Ve a la pestaña API Groq.",
    },
    "engine.error.badkey": {
        "en": "Invalid Groq key — must start with gsk_ (from console.groq.com).",
        "fr": "Clé Groq invalide — doit commencer par gsk_ (console.groq.com).",
        "es": "Clave Groq inválida — debe empezar con gsk_ (console.groq.com).",
    },
    "agent.started": {
        "en": "OS agent active",
        "fr": "Agent OS actif",
        "es": "Agente del sistema activo",
    },
    "agent.stopped": {
        "en": "OS agent stopped",
        "fr": "Agent OS arrêté",
        "es": "Agente del sistema detenido",
    },
    "agent.listening": {
        "en": "Agent listening…",
        "fr": "Agent à l'écoute…",
        "es": "Agente escuchando…",
    },
}

# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

def tr(key: str) -> str:
    """Return the translation of *key* in the current UI language.

    Reads ``UI_LANGUAGE`` from :class:`~acouz.utils.config.ConfigManager` on
    every call so language switches take effect immediately without requiring a
    restart.  Falls back to Spanish if the current language or key is not found.

    Args:
        key: Dot-separated string key defined in :data:`_STRINGS`.

    Returns:
        The translated string, or *key* itself if no entry is found.
    """
    # Import here to avoid a module-level circular dependency in tests.
    from acouz.utils.config import ConfigManager  # noqa: PLC0415

    lang = ConfigManager.get("UI_LANGUAGE", "es")
    entry = _STRINGS.get(key, {})
    return entry.get(lang) or entry.get("es") or entry.get("en") or key
