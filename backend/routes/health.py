"""
Health Check Routes

Handles health check and system status endpoints
"""

from fastapi import APIRouter, Request
from slowapi.util import get_remote_address
import time
import logging
import os
from typing import Optional

from config import settings
from storage import storage

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """Enhanced health check for production"""
    try:
        # Check if API key is configured (safely)
        api_key_configured = bool(getattr(settings, 'MISTRAL_API_KEY', None))
        if not api_key_configured:
            return {"status": "unhealthy", "error": "API key not configured"}
        
        # Check storage
        storage_stats = storage.get_storage_stats()
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "environment": os.getenv("ENVIRONMENT", "development"),
            "storage": storage_stats
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@router.get("/status")
async def system_status(request: Request):
    """
    Detailed system status endpoint
    
    Returns:
        System status with storage statistics
    """
    try:
        stats = storage.get_storage_stats()
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "storage": stats
        }
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        return {
            "status": "error",
            "timestamp": time.time(),
            "error": "Failed to retrieve system status"
        }
