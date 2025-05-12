import sys
import os
import logging
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info(f"Project root set to: {project_root}")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python path: {sys.path}")

# Create necessary directories
for dir_path in ["logs", "Data", "audio", "templates", "static"]:
    try:
        Path(dir_path).mkdir(exist_ok=True)
        logger.info(f"Directory exists or created: {dir_path}")
    except Exception as e:
        logger.warning(f"Failed to create directory {dir_path}: {str(e)}")

try:
    # Import main app
    from api.main import create_app
    app = create_app()
except Exception as e:
    logger.error(f"Error initializing app: {str(e)}")
    raise

# Vercel handler
handler = app

### s:\Projects\FastAPI\SeperateFolder\MyraChatBot\README.md

