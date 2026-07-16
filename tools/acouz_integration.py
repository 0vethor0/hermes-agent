"""
AcouZ (Voiceless) Integration for Hermes Agent
"""
from __future__ import annotations
import sys
import threading
import json
from pathlib import Path
from typing import Optional

# Add tools directory to sys.path to allow "import acouz"
tools_dir = Path(__file__).parent.resolve()
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

# Lazy import for acouz dependencies
try:
    from tools.lazy_deps import ensure
    ensure("tool.acouz", prompt=False)
except Exception:
    pass


class AcouZIntegration:
    """Integration wrapper for AcouZ (Voiceless) application"""
    
    _instance: Optional["AcouZIntegration"] = None
    _app_thread: Optional[threading.Thread] = None
    _is_running: bool = False
    _process = None  # To store the QApplication instance
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True
    
    def initialize(self):
        """Initialize AcouZ configuration and components"""
        try:
            from acouz.utils.config import ConfigManager
            ConfigManager.initialize()
            return True
        except Exception as e:
            print(f"Error initializing AcouZ config: {e}", file=sys.stderr)
            return False
    
    def open_ui(self):
        """Open AcouZ main UI window"""
        if self._is_running:
            print("AcouZ UI already running")
            return
        
        def _run_acouz():
            try:
                from acouz.ui.app import AcouZApp
                from PySide6.QtWidgets import QApplication
                
                # Initialize config
                self.initialize()
                
                # Create and run Qt app
                app = QApplication.instance()
                if app is None:
                    app = QApplication(sys.argv)
                
                window = AcouZApp()
                window.show()
                
                self._is_running = True
                app.exec()
                self._is_running = False
                
            except Exception as e:
                print(f"Error running AcouZ UI: {e}", file=sys.stderr)
                self._is_running = False
        
        self._app_thread = threading.Thread(target=_run_acouz, daemon=True)
        self._app_thread.start()
    
    def is_running(self):
        """Check if AcouZ UI is currently running"""
        return self._is_running
    
    def get_config(self, key: str, default: str = ""):
        """Get a value from AcouZ config"""
        try:
            from acouz.utils.config import ConfigManager
            ConfigManager.initialize()
            return ConfigManager.get(key, default)
        except Exception as e:
            print(f"Error getting config: {e}", file=sys.stderr)
            return default
    
    def set_config(self, key: str, value: any):
        """Set a value in AcouZ config"""
        try:
            from acouz.utils.config import ConfigManager
            ConfigManager.initialize()
            ConfigManager.set(key, value)
            return True
        except Exception as e:
            print(f"Error setting config: {e}", file=sys.stderr)
            return False


# Singleton instance
acouz = AcouZIntegration()


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python -m tools.acouz_integration <command> [args]", file=sys.stderr)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "open":
        acouz.open_ui()
        # Keep the process alive while the UI is running
        try:
            if acouz._app_thread:
                acouz._app_thread.join()
        except KeyboardInterrupt:
            pass
    elif command == "is_running":
        print(json.dumps({"running": acouz.is_running()}))
    elif command == "get_config":
        key = sys.argv[2]
        default = sys.argv[3] if len(sys.argv) > 3 else ""
        value = acouz.get_config(key, default)
        print(json.dumps({"value": value}))
    elif command == "set_config":
        key = sys.argv[2]
        value = json.loads(sys.argv[3])
        success = acouz.set_config(key, value)
        print(json.dumps({"success": success}))
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()