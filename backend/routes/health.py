"""
Health Check Routes

Handles health check and system status endpoints
"""

from fastapi import APIRouter, Request
from slowapi.util import get_remote_address
import time
import logging

from config import settings
from storage import storage

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check(request: Request):
    """
    Basic health check endpoint
    
    Returns:
        Health status with timestamp
    """
    return {
        "status": "healthy", 
        "timestamp": time.time()
    }

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
