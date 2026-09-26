import threading
import logging
from UI.widget import SpothashWidget
from core.duck import monitor_audio
from core.tray import SystemTrayManager

logger = logging.getLogger(__name__)

class AppController:
    """
    app threads: Audio monitoring worker,
    System Tray icon manager, and Tkinter media widget GUI.
    """
    def __init__(self):
        self.is_running = True
        self.stop_event = threading.Event()
        
        # Initialize Core Modules
        self.audio_thread = threading.Thread(
            target=monitor_audio,
            args=(self.stop_event,),
            daemon=True
        )
        self.tray_manager = SystemTrayManager(quit_callback=self.stop_application)
        self.widget = SpothashWidget(on_close_callback=self.stop_application)

    def stop_application(self):
        if self.is_running:
            self.is_running = False
            # Stop system tray icon
            self.tray_manager.stop()
            # Signal the monitor_audio loop to stop and wait for cleanup
            self.stop_event.set()
            if self.audio_thread.is_alive():
                self.audio_thread.join(timeout=2.0)
            # Safely quit Tkinter mainloop if running
            try:
                self.widget.root.quit()
            except Exception:
                pass

    def run(self):
        self.audio_thread.start()
        self.tray_manager.start()
        self.widget.run()