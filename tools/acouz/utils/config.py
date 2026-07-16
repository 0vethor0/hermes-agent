"""
AcouZ - Open-source AI voice dictation
Copyright (c) 2025-2026 DoodzProg
Licensed under the MIT License

Configuration management for the AcouZ application.

Configuration is persisted in a ``config.json`` file located in the same 
directory as the executable (when frozen) or in the project root 
(during development). For backward compatibility, it also attempts 
to migrate settings from a ``.env`` file.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

try:
    from dotenv import dotenv_values
except ImportError:
    dotenv_values = None

# ------------------------------------------------------------------
# ConfigManager
# ------------------------------------------------------------------

class ConfigManager:
    """Static helper class for reading and writing user configuration.

    Configuration is persisted in a ``config.json`` file and exposed as OS environment
    variables so that any third-party library relying on ``os.getenv`` (e.g.
    the Groq SDK) picks up the values automatically.

    All methods are ``@staticmethod`` — there is no instance state.
    """

    _CONFIG_FILE: Path = None
    _DATA: dict = {}

    @staticmethod
    def initialize() -> None:
        """Load configuration from config.json and migrate from .env if necessary.

        Should be called once at application startup.
        """
        if getattr(sys, "frozen", False):
            # Running from an exe: config is next to the executable
            base_dir = Path(sys.executable).parent
        else:
            # Running in hermes-agent: config is in hermes-agent root
            # Path(__file__) is tools/acouz/utils/config.py
            # .parent is tools/acouz/utils
            # .parent.parent is tools/acouz
            # .parent.parent.parent is tools
            # .parent.parent.parent.parent is project root
            base_dir = Path(__file__).resolve().parent.parent.parent.parent

        ConfigManager._CONFIG_FILE = base_dir / "config.json"

        # 1. If frozen and no config.json exists next to the exe,
        #    copy the bundled default from the PyInstaller temp directory.
        if getattr(sys, "frozen", False) and not ConfigManager._CONFIG_FILE.exists():
            bundled = Path(sys._MEIPASS) / "config.default.json"
            if bundled.exists():
                try:
                    shutil.copy2(str(bundled), str(ConfigManager._CONFIG_FILE))
                except Exception:
                    pass

        # 2. Load config.json if it exists
        if ConfigManager._CONFIG_FILE.exists():
            try:
                with open(ConfigManager._CONFIG_FILE, 'r', encoding='utf-8') as f:
                    ConfigManager._DATA = json.load(f)
            except Exception:
                ConfigManager._DATA = {}
        else:
            ConfigManager._DATA = {}

        # 3. Backward compatibility: Migrate from .env if it exists
        env_path = base_dir / ".env"
        if env_path.exists():
            if dotenv_values:
                env_data = dotenv_values(dotenv_path=str(env_path))
                if env_data:
                    new_data = False
                    for k, v in env_data.items():
                        if k not in ConfigManager._DATA:
                            ConfigManager._DATA[k] = v
                            new_data = True
                    if new_data:
                        ConfigManager._save()

        # 4. Update os.environ for compatibility
        for k, v in ConfigManager._DATA.items():
            os.environ[k] = str(v)

    @staticmethod
    def _save() -> None:
        """Persist the current in-memory configuration to config.json."""
        if ConfigManager._CONFIG_FILE:
            try:
                ConfigManager._CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(ConfigManager._CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump(ConfigManager._DATA, f, indent=4)
            except Exception:
                pass

    @staticmethod
    def get(key: str, default: str = "") -> str:
        """Return the value for *key* as a string, or *default* if it is not set.

        Args:
            key:     Configuration key (e.g. ``"GROQ_API_KEY"``).
            default: Fallback value when the key is absent (default ``""``).

        Returns:
            The string value associated with *key*, or *default*.
        """
        return str(ConfigManager._DATA.get(key, default))

    @staticmethod
    def set(key: str, value: any) -> None:
        """Persist *value* for *key* in config.json and update the live environment.

        Args:
            key:   Configuration key.
            value: Value to store.

        Raises:
            OSError: If the config.json file cannot be written.
        """
        ConfigManager._DATA[key] = value
        ConfigManager._save()
        os.environ[key] = str(value)

    @staticmethod
    def get_all_keys() -> list[str]:
        """Return all currently loaded configuration keys.

        Returns:
            A list of configuration key names.
        """
        return list(ConfigManager._DATA.keys())
