"""
Logging utility for the training orchestration system.
"""
import logging
import os
from datetime import datetime
from config.settings import Settings

def setup_logger(name: str) -> logging.Logger:
    """
    Setup logger with file and console handlers.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Create logs directory if it doesn't exist
    os.makedirs(Settings.LOG_DIRECTORY, exist_ok=True)
    
    # File handler
    log_filename = os.path.join(
        Settings.LOG_DIRECTORY,
        f"{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


# Create module logger
logger = setup_logger(__name__)
