"""
Logger Utility for AutoMoM
--------------------------
Centralized logging system using Loguru.
"""

from loguru import logger
import os

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define log file path
LOG_FILE = os.path.join(LOG_DIR, "running_logs.log")

# Remove old handlers (avoid duplicates)
logger.remove()

# Configure loguru logger
logger.add(
    LOG_FILE,
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="1 MB",
    compression="zip",
)

__all__ = ["logger"]

# Example usage:
# from automom.utils.logger import logger
# logger.info("✅ Logging initialized successfully!")
