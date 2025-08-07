# app/utils/logging.py

import logging
from logging.handlers import RotatingFileHandler
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_DIR = os.environ.get("LOG_DIR", "./logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str = "llm_query_system") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # prevent duplicate logs in uvicorn multi-workers
    if not logger.hasHandlers():
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(LOG_LEVEL)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # Rotating file handler (10MB max per file, keep last 5)
        fh = RotatingFileHandler(LOG_FILE, maxBytes=10_485_760, backupCount=5)
        fh.setLevel(LOG_LEVEL)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
