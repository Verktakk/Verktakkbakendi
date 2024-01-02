import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s", "%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler("logs/app.log", maxBytes=10000000, backupCount=5)
    file_handler.setFormatter(log_formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)