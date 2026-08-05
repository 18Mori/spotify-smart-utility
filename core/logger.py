import logging

class ColoredFormatter(logging.Formatter):
    # ANSI Color Palette
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    LEVEL_COLORS = {
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: BOLD + RED,
    }

    def formatTime(self, record, datefmt=None):
        return super().formatTime(record, datefmt)

    def format(self, record, datefmt=None):
        formatted_time = self.formatTime(record, datefmt)
        colored_time = f"{self.CYAN}{formatted_time}{self.RESET}"

        level_color = self.LEVEL_COLORS.get(record.levelno, self.RESET)
        colored_level = f"{level_color}{record.levelname}{self.RESET}"

        return f"{colored_time} [{colored_level}] {record.getMessage()}"

def setup_logging():
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)