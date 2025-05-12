from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import sys
# Add project root to path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from routes import chat_routes

router = APIRouter()
# Check if templates directory exists
if os.path.isdir("templates"):
    templates = Jinja2Templates(directory="templates")
else:
    # Create a simple Jinja2Templates object to avoid runtime errors
    templates = Jinja2Templates(directory=".")

@router.get("/hello")
async def hello_world():
    """
    Simple test endpoint to verify API routes are working
    """
    return {"message": "Hello World! The API is working correctly."}

# Include all route modules
router.include_router(chat_routes.router, tags=["chat"])
