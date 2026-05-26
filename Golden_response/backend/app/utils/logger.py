import logging
import os

# Create log directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Formatter
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(os.path.join(LOG_DIR, log_file))
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Avoid duplicate logs if the logger already has handlers
    if not logger.handlers:
        logger.addHandler(handler)
        # Also log to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

app_logger = setup_logger("app", "app.log")
error_logger = setup_logger("error", "errors.log", level=logging.ERROR)
submission_logger = setup_logger("submissions", "submissions.log")
