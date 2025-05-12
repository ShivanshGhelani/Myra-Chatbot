from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import chat_routes

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Include all route modules
router.include_router(chat_routes.router, tags=["chat"])
