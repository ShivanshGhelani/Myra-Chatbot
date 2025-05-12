"""
Vercel serverless function entry point using FastAPI
"""
import sys
import os
from pathlib import Path
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
logger.info(f"Project root added to path: {parent_dir}")

# Create writable directories in /tmp if on Vercel
if os.environ.get('VERCEL') == '1':
    tmp_dir = Path("/tmp")
    for dir_path in ["logs", "data", "audio"]:
        try:
            (tmp_dir / dir_path).mkdir(exist_ok=True, parents=True)
            logger.info(f"Created temp directory: {str(tmp_dir / dir_path)}")
        except Exception as e:
            logger.warning(f"Failed to create directory: {str(e)}")

# Import FastAPI app
try:
    from fastapi import FastAPI, Request, Response
    from api.main import create_app
    logger.info("Successfully imported FastAPI and main app")
except Exception as e:
    logger.error(f"Error importing FastAPI modules: {str(e)}")
    raise

# Create the FastAPI application
app = None
try:
    app = create_app()
    logger.info("FastAPI application created successfully")
except Exception as e:
    logger.error(f"Error creating FastAPI app: {str(e)}")
    raise

# This is what Vercel looks for to handle requests
from http.server import BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "success",
            "message": "FastAPI application is running",
            "endpoints": {
                "API Root": "/",
                "Health Check": "/health",
                "Environment Check": "/env-check"
            }
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
        
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "success", 
            "message": "POST requests are supported, but this is a basic handler",
            "note": "For full FastAPI functionality, configure your Vercel project to use this as an API endpoint"
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
