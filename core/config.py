import os 
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
  def __init__(self, filename="ignored_apps.txt"):
    self.filename = self.resolve_root_path(filename)
    self.last_mod_time = 0 # tracks the last modification time of the config file
    self.ignored_apps = set()
    
  def resolve_root_path(self, filename: str) -> str:
    if os.path.exists(filename):
      return os.path.abspath(filename)
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the configuration file
    config_path = os.path.join(os.path.dirname(base_dir), filename)
    return config_path # fallback to the default path if the file is not found in the current directory.
  
  def load_ignored_apps(self) -> set[set]:
    if not os.path.exists(self.filename):
      if self.ignored_apps:
        logger.warning("Configuration file %s not found. No apps will be ignored.", self.filename)
        self.ignored_apps.clear()
        self.last_mod_time = 0
        return self.ignored_apps
      
    try:
      current_mod_time = os.path.getmtime(self.filename)
      if current_mod_time != self.last_mod_time:
        new_ignored_app = set()
        with open(self.filename, "r", encoding="utf-8") as f:
          for line in f:
            clean_line = line.strip().lower()
            if clean_line and not clean_line.startswith("#"):
              new_ignored_app.add(clean_line)
              
        self.ignored_apps = new_ignored_app
        self.last_mod_time = current_mod_time
        logger.info("Reload apps from %s: %s, now ignored %d app(s).", self.filename, self.ignored_apps, len(self.ignored_apps))
    except Exception as e:
      logger.warning("Could not read %s: %s", self.filename, e)
    return self.ignored_apps