"""
FastAPI Application Setup

This module handles the FastAPI application configuration,
middleware setup, and route registration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging

from config import settings
from routes import health, ingest, query

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    # Create rate limiter
    limiter = Limiter(key_func=get_remote_address)
    
    # Create FastAPI app
    app = FastAPI(
        title="RAG System API",
        description="A simple RAG pipeline for PDF document processing",
        version="1.0.0"
    )
    
    # Add rate limiter to app
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],  # Only allow needed methods
        allow_headers=["Content-Type", "Authorization"],  # Only allow needed headers
    )
    
    # Include route modules
    app.include_router(health.router)
    app.include_router(ingest.router)
    app.include_router(query.router)
    
    logger.info("FastAPI application configured successfully")
    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
