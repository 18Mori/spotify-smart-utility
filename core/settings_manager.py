import os
import json
import logging

logger = logging.getLogger(__name__)

class SettingsManager:
    """
    Manages local JSON persistence for user preferences (e.g., startup toggle state).
    """
    def __init__(self, filename="settings.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.join(os.path.dirname(base_dir), filename)
        self.settings = self.load_settings()

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
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            logger.error("Could not save settings to %s: %s", self.filepath, e)
            return False

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
