"""
Vercel Python WSGI/ASGI entry point
"""
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    # Import the FastAPI app
    from api.main import create_app
    
    # Create the application instance
    app = create_app()
    
    # Export as handler for Vercel (both names are used in different Vercel Python examples)
    handler = app
    app_handler = app
    
    logger.info("FastAPI application loaded successfully in index.py")
except Exception as e:
    logger.error(f"Failed to initialize FastAPI app in index.py: {str(e)}")
    raise
