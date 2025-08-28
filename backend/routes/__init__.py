"""
Routes Package

This package contains all API route handlers organized by functionality.
Each module handles a specific set of related endpoints.
"""

from . import health
from . import ingest
from . import query

__all__ = [
    'health',
    'ingest', 
    'query'
]
