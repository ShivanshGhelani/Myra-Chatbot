from dotenv import load_dotenv
import os
from typing import Optional, Dict
from pathlib import Path

class Settings:
    def __init__(self):
        # Load environment variables from .env file if it exists
        load_dotenv()
        
        # Get environment variables from both .env file and system environment
        self.env_vars = self._get_env_vars()
        self._validate_required_env_vars()
        self.USERNAME = self.env_vars.get("Username", "Assistant")
        self.ASSISTANT_NAME = self.env_vars.get("Assistantname", "AI Assistant")
        self.GROQ_API_KEY = self.get_required_env_var("GroqAPIKey")
        
        # Check if running on Vercel for path settings
        self.IS_VERCEL = os.environ.get('VERCEL') == '1'
        
        # Set appropriate paths based on environment
        if self.IS_VERCEL:
            # Use /tmp directory for Vercel (serverless functions can write here)
            self.CHAT_LOG_PATH = "/tmp/data/ChatLog.json"
            self.SPEECH_FILE_PATH = "/tmp/speech.mp3"
        else:
            # Local paths
            self.CHAT_LOG_PATH = "Data/ChatLog.json"
            self.SPEECH_FILE_PATH = "speech.mp3"
    
    def _get_env_vars(self) -> Dict[str, str]:
        """Combine environment variables from both .env file and system environment."""
        # Priority: system environment variables override .env file
        env_vars = {}
        
        # Add all system environment variables
        for key, value in os.environ.items():
            env_vars[key] = value
            
        return env_vars
    def _validate_required_env_vars(self) -> None:
        """Validate that all required environment variables are present."""
        required_vars = ["GroqAPIKey"]
        missing_vars = []
        
        for var in required_vars:
            # Check both system env vars and .env file
            if not self.env_vars.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                "Please check your environment variables or .env file."
            )
    
    def get_required_env_var(self, key: str) -> str:
        """Get a required environment variable or raise an error if it's missing."""
        # Check for environment variable in system environment or .env file
        value = self.env_vars.get(key)
        if not value:
            raise EnvironmentError(f"Missing required environment variable: {key}")
        return value

# Initialize settings with error handling
try:
    settings = Settings()
except Exception as e:
    print(f"Failed to initialize settings: {str(e)}")
    raise

# Base directory
BASE_DIR = Path(__file__).parent.parent
IS_VERCEL = os.environ.get('VERCEL') == '1'

# Set up directories based on environment
if IS_VERCEL:
    import tempfile
    # Use /tmp directory which is writable on Vercel
    TMP_DIR = Path('/tmp')

    LOGS_DIR = TMP_DIR / 'logs'
    DATA_DIR = TMP_DIR / 'data'
    TEMPLATES_DIR = BASE_DIR / 'templates'  # Read-only is fine for templates
else:

    LOGS_DIR = BASE_DIR / 'logs'
    DATA_DIR = BASE_DIR / 'Data'
    TEMPLATES_DIR = BASE_DIR / 'templates'

# Language settings
DEFAULT_LANGUAGE = 'en-US'
SUPPORTED_LANGUAGES = ['gu-IN', 'hi-IN', 'en-US', 'fr-FR', 'es-ES', 'de-DE', 'it-IT', 'ja-JP', 'ko-KR', 'zh-CN', 'ru-RU']

# Ensure directories exist in writable locations
try:
    if not IS_VERCEL:
        LOGS_DIR.mkdir(exist_ok=True)
        DATA_DIR.mkdir(exist_ok=True)
except Exception as e:
    print(f"Warning: Could not create directories: {str(e)}")
    # Fall back to memory-only operation if directories can't be created