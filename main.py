from core.logger import setup_logging
from core.controller import AppController

if __name__ == "__main__":
    setup_logging()
    
    app = AppController()
    app.run()