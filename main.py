from ui.widget import SpothashWidget


class AppController:
    def __init__(self):
        self.is_running = True
        
        # Initialize Core Modules
        self.widget = SpothashWidget(on_close_callback=self.stop_application)
        

    def stop_application(self):
        self.is_running = False

    def run(self):
        self.widget.run()


if __name__ == "__main__":
    app = AppController()
    app.run()