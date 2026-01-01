import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "AI Interview Backend API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".pdf", ".txt"]
    
    # Interview Settings
    DEFAULT_TOTAL_QUESTIONS: int = 10
    REPEAT_WINDOW_SECONDS: int = 120
    RECORD_MAX_TIME_SECONDS: int = 300
    STOP_BUTTON_TIME_SECONDS: int = 90
    PREVIEW_TIME_SECONDS: int = 20
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
