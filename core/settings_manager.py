import os
import sys
import json
import logging

logger = logging.getLogger(__name__)

class SettingsManager:
    """
    Manages local JSON persistence for user preferences (e.g., startup toggle state).
    Stores settings in a persistent user application data directory to ensure
    persistence across launches in PyInstaller standalone builds.
    """
    def __init__(self, filename="settings.json"):
        self.filepath = self.resolve_settings_path(filename)
        self.settings = self.load_settings()

    def resolve_settings_path(self, filename: str) -> str:
        # Check if local settings.json already exists (portable / development mode)
        if os.path.exists(filename):
            return os.path.abspath(filename)
            
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            exe_local_path = os.path.join(exe_dir, filename)
            if os.path.exists(exe_local_path):
                return exe_local_path
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            script_local_path = os.path.join(os.path.dirname(base_dir), filename)
            if os.path.exists(script_local_path):
                return script_local_path

        # Default to persistent per-user application data directory
        if os.name == 'nt':
            app_data = os.getenv('APPDATA')
            base_dir = os.path.join(app_data, 'SpotHash') if app_data else os.path.expanduser('~/.spothash')
        else:
            base_dir = os.path.expanduser('~/.config/spothash')

        try:
            os.makedirs(base_dir, exist_ok=True)
        except Exception as e:
            logger.warning("Could not create config directory %s: %s", base_dir, e)

        return os.path.join(base_dir, filename)

    def load_settings(self) -> dict:
        default_settings = {"startup_enabled": False}
        if not os.path.exists(self.filepath):
            return default_settings
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    default_settings.update(data)
        except Exception as e:
            logger.warning("Could not load settings from %s: %s", self.filepath, e)
        return default_settings

    def save_settings(self) -> bool:
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            logger.error("Could not save settings to %s: %s", self.filepath, e)
            return False

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value) -> bool:
        self.settings[key] = value
        return self.save_settings()
