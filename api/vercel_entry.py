import sys
import os
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create necessary directories
for dir_path in ["logs", "Data", "audio", "templates", "static"]:
    Path(dir_path).mkdir(exist_ok=True)

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

