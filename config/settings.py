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

# Supported audio formats
SUPPORTED_FORMATS = ('.wav', '.aiff', '.aif', '.flac', '.mp3', '.ogg', '.opus', '.m4a', '.aac')

# Audio directory for saving uploaded files
AUDIO_DIR = BASE_DIR / 'audio'

# Language settings
DEFAULT_LANGUAGE = 'en-US'
SUPPORTED_LANGUAGES = ['gu-IN', 'hi-IN', 'en-US', 'fr-FR', 'es-ES', 'de-DE', 'it-IT', 'ja-JP', 'ko-KR', 'zh-CN', 'ru-RU']

# Directory settings
AUDIO_DIR = BASE_DIR / 'audio'
TEMPLATES_DIR = BASE_DIR / 'templates'

# Ensure directories exist
AUDIO_DIR.mkdir(exist_ok=True)