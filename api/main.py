from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routes import router  # Use relative import
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.WARNING)  # Set global logging level to WARNING
# Suppress specific loggers
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("pygame").setLevel(logging.WARNING)

def create_app():
    app = FastAPI()

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
    if os.path.isdir("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")
    if os.path.isdir("templates"):
        app.mount("/templates", StaticFiles(directory="templates"), name="templates")

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        if os.path.exists("static/SVG/bot.svg"):
            return FileResponse("static/SVG/bot.svg")
        return None

    @app.get("/", response_class=HTMLResponse)
    async def read_root():
        if os.path.exists("templates/bot.html"):
            with open("templates/bot.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read(), status_code=200)
        return HTMLResponse(content="<h1>Myra ChatBot API</h1><p>API is running. Use endpoints to interact with the chatbot.</p>")

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
