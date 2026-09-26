import threading
import logging
from PIL import Image, ImageDraw
import pystray
from core.startup_manager import StartupManager
from core.settings_manager import SettingsManager

logger = logging.getLogger(__name__)

class SystemTrayManager:
    """
    Manages the Windows taskbar system tray icon (next to Wi-Fi and volume)
    providing a clean context menu for Startup preferences and Application Exit.
    """
    def __init__(self, quit_callback=None):
        self.quit_callback = quit_callback
        self.startup_manager = StartupManager()
        self.settings_manager = SettingsManager()
        self.icon = None
        self._thread = None

    def create_icon_image(self):
        # Create a dynamic Spotify green themed system tray icon
        image = Image.new('RGB', (64, 64), color="#191414")
        dc = ImageDraw.Draw(image)
        # Draw green accent square
        dc.rectangle([12, 12, 52, 52], fill="#1DB954")
        # Draw inner symbol 'S'
        dc.text((24, 20), "S", fill="#191414")
        return image

    def on_startup_toggled(self, icon, item):
        current_state = self.settings_manager.get("startup_enabled", False)
        new_state = not current_state
        success = self.startup_manager.set_startup(new_state)
        if success:
            self.settings_manager.set("startup_enabled", new_state)
            logger.info("System startup toggled from tray to: %s", new_state)
        else:
            logger.error("Failed to toggle system startup from tray.")

    def get_startup_checked(self, item):
        return self.settings_manager.get("startup_enabled", False)

    def on_quit(self, icon, item):
        if self.icon:
            self.icon.stop()
        if callable(self.quit_callback):
            self.quit_callback()

    def run(self):
        image = self.create_icon_image()
        menu = pystray.Menu(
            pystray.MenuItem("SpotHash Media Widget", lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Launch on System Startup",
                self.on_startup_toggled,
                checked=self.get_startup_checked
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.on_quit)
        )
        self.icon = pystray.Icon("SpotHash", image, "SpotHash Media Widget", menu)
        self.icon.run()

    def start(self):
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()
        logger.info("System tray icon started.")

    def stop(self):
        if self.icon:
            try:
                self.icon.stop()
            except Exception:
                pass
