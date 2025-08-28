import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    MISTRAL_API_KEY: Optional[str] = None  # Optional for development
    MISTRAL_BASE_URL: str = "https://api.mistral.ai/v1"
    
    # File Storage
    DATA_DIR: str = "data"
    UPLOAD_DIR: str = "data/uploads"
    
    # RAG Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_CHUNKS_PER_DOC: int = 50
    
    # Search Configuration
    TOP_K_RESULTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    
    # LLM Configuration
    MODEL_NAME: str = "mistral-large-latest"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.1
    
    # Rate Limiting Configuration
    RATE_LIMIT_QUERY: str = "30/minute"
    RATE_LIMIT_UPLOAD: str = "10/minute"
    RATE_LIMIT_HEALTH: str = "60/minute"
    
    class Config:
        env_file = "../.env"

# Global settings instance
settings = Settings()



# Ensure directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
