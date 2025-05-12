import sys
import os
import logging

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import FastAPI app
try:
    from api.main import create_app
    app = create_app()
    logger.info("WSGI app created successfully")
except Exception as e:
    logger.error(f"Error initializing WSGI app: {str(e)}")
    raise

# For Vercel - handler must be a WSGI app (not FastAPI)
def handler(environ, start_response):
    """
    Simple WSGI handler that forwards to the FastAPI application
    """
    logger.info(f"WSGI handler called with path: {environ.get('PATH_INFO', '/')}")
    
    # This is just a debug response to test if the handler works
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b"WSGI Handler Reached - This is just a test. Update vercel.json to use the real app."]
