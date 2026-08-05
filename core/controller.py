import threading
from UI.widget import SpothashWidget
from core.duck import monitor_audio


class AppController:
    def __init__(self):
        self.is_running = True
        
        self.stop_event = threading.Event()
        
        # Initialize Core Modules
        self.audio_thread = threading.Thread(
            target=monitor_audio,
            args=(self.stop_event,),
            daemon=True
        )
        self.widget = SpothashWidget(on_close_callback=self.stop_application)

    def stop_application(self):
        if self.is_running:
            self.is_running = False
            # Signal the monitor_audio loop to stop and wait for it to clean up volume
            self.stop_event.set()
            if self.audio_thread.is_alive():
                self.audio_thread.join(timeout=2.0)

    def run(self):
        self.audio_thread.start()
        self.widget.run()