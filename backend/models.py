"""
Models Module - Legacy Import Interface

This file provides backward compatibility imports for the refactored models.
All models are now organized in the core/models package for better maintainability.

For new code, import directly from core.models:
    from core.models import QueryRequest, QueryResponse, QueryValidator
"""

# Import all models from the new modular structure
from core.models import (
    # Request models
    FileUploadRequest,
    QueryRequest,
    
    # Response models
    QueryResponse,
    UploadResponse,
    ChunkInfo,
    DocumentInfo,
    
    # Internal models
    Document,
    SearchResult,
    
    # Validators
    QueryValidator
)

# Re-export for backward compatibility
__all__ = [
    'FileUploadRequest',
    'QueryRequest',
    'QueryResponse',
    'UploadResponse',
    'ChunkInfo',
    'DocumentInfo',
    'Document',
    'SearchResult',
    'QueryValidator'
]
