import logging
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_file_path = os.path.join(LOG_DIR, "app.log")

# JSON formatter
json_formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(lineno)d'
)

# File handler with rotation
file_handler = RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(json_formatter)

# Stream (console) handler with same format
console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)

# Root logger setup
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.propagate = False
