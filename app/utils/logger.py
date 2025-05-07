import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure the logger
logger = logging.getLogger("marvel_genetics")
logger.setLevel(settings.LOG_LEVEL)

# Create formatters
console_formatter = logging.Formatter(
    '%(levelname)s:     %(message)s'
)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler with rotation
file_handler = RotatingFileHandler(
    log_dir / "app.log",
    maxBytes=10_000_000,  # 10MB
    backupCount=5
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Prevent propagation to root logger
logger.propagate = False
