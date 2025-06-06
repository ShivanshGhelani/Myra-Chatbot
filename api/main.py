from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import sys
from pathlib import Path

# Handle imports correctly whether run as a module or directly
try:
    from .routes import router  # Try relative import (when imported as a module)
except ImportError:
    # If that fails, try to add parent directory to path for direct script execution
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from api.routes import router  # Absolute import (when run directly)

# Configure logging
logging.basicConfig(level=logging.WARNING)  # Set global logging level to WARNING
# Suppress specific loggers
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("pygame").setLevel(logging.WARNING)

def create_app():
    app = FastAPI(
        title="Myra ChatBot API",
        description="FastAPI application for Myra ChatBot",
        version="1.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    # Mount static directories if they exist
    # Try both absolute and relative paths for static directories
    static_paths = ["static", os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")]
    template_paths = ["templates", os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")]
    for path in static_paths:
        if os.path.isdir(path):
            logging.info(f"Mounting static directory at: {path}")
            app.mount("/static", StaticFiles(directory=path), name="static")
            break
    
    for path in template_paths:
        if os.path.isdir(path):
            logging.info(f"Mounting templates directory at: {path}")
            app.mount("/templates", StaticFiles(directory=path), name="templates")
            break
            
    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        # Try multiple potential paths for favicon
        favicon_paths = [
            "static/SVG/bot.svg",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/SVG/bot.svg"),
            "static/favicon.ico",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/favicon.ico")
        ]
        
        for path in favicon_paths:
            if os.path.exists(path):
                logging.info(f"Serving favicon from: {path}")
                return FileResponse(path)
            logging.warning("Favicon not found")
        return None
        
    @app.get("/", response_class=HTMLResponse)
    async def read_root():
        # Try multiple potential paths for the template file
        template_paths = [
            "templates/bot.html",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates/bot.html")
        ]
        
        for path in template_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        logging.info(f"Loading template from: {path}")
                        return HTMLResponse(content=f.read(), status_code=200)
                except Exception as e:
                    logging.error(f"Error reading template file {path}: {str(e)}")
          # Fallback HTML content
        logging.warning("Template file not found, serving default HTML")
        return HTMLResponse(content="<h1>Myra ChatBot API</h1><p>API is running. Use endpoints to interact with the chatbot.</p>")
        
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
        
    @app.get("/env-check")
    async def env_check():
        """Check environment variables (non-sensitive ones)"""
        # Only show non-sensitive information
        env_info = {
            "VERCEL": os.environ.get("VERCEL"),
            "is_vercel": os.environ.get("VERCEL") == "1",
            "temp_writable": os.access("/tmp", os.W_OK),
            "api_keys_available": bool(os.environ.get("GroqAPIKey")),
            "writable_dirs": {
                "/tmp": os.access("/tmp", os.W_OK),
                "audio": os.access("/tmp/audio" if os.environ.get("VERCEL") == "1" else "audio", os.W_OK),
                "data": os.access("/tmp/data" if os.environ.get("VERCEL") == "1" else "Data", os.W_OK) 
            }
        }
        return env_info

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
