import logging

# Configure logging
logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %I:%M:%S %p',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Optional: Create a logger instance (useful for modular logging)
logger = logging.getLogger(__name__)
logger.debug("Logging system initialized.")