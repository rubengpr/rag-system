"""
FastAPI Application Setup

This module handles the FastAPI application configuration,
middleware setup, and route registration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from config import settings
from routes import health, ingest, query

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    # Create FastAPI app
    app = FastAPI(
        title="RAG System API",
        description="A simple RAG pipeline for PDF document processing",
        version="1.0.0"
    )
    
    # Configure CORS origins based on environment
    allowed_origins = [
        "http://localhost:3000", 
        "http://localhost:5173",
        "https://rag-system-bay.vercel.app"
    ]
    
    # Add production origins if they exist
    if os.getenv("FRONTEND_URL"):
        allowed_origins.append(os.getenv("FRONTEND_URL"))
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
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
