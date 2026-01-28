import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name="autodoc"):
    # Ensure log directory exists
    log_dir = Path(".autodoc/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if setup called multiple times
    if logger.handlers:
        return logger

    # Formatting
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 1. File Handler (Rotating)
    # writes to .autodoc/logs/autodoc.log
    file_handler = RotatingFileHandler(
        log_dir / "autodoc.log",
        maxBytes=1024 * 1024,  # 1MB
        backupCount=3,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 2. Console Handler (Standard Output)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
