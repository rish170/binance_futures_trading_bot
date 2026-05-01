import logging
from rich.logging import RichHandler

def setup_logger():
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger

    file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler("trading_bot.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    console_handler = RichHandler(rich_tracebacks=True, show_path=False)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()

def log_separator():
    """Adds a newline separator to the log file."""
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.stream.write("\n")
            handler.stream.flush()
