# app/config/simple_settings.py
import os
from typing import Optional

class SimpleSettings:
    """Ultra-simple settings without pydantic-settings to avoid dependencies"""
    
    def __init__(self):
        # App Settings
        self.app_name = "HackRX LLM API"
        self.debug = True
        
        # Server
        self.host = "0.0.0.0"
        self.port = int(os.getenv("PORT", 8000))
        
        # API Keys (optional for deployment)
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "dummy-key")
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY", "dummy-key")
        
        # Environment
        self.environment = os.getenv("APP_ENV", "production")

# Global settings instance
settings = SimpleSettings()
