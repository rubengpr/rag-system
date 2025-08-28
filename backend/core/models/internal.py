"""
Internal Models

Contains internal business logic models not exposed to the API.
These models are used for internal processing and data management.
"""

from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from .responses import ChunkInfo

class Document(BaseModel):
    """Internal document representation"""
    id: UUID
    filename: str
    content: str
    chunks: List[ChunkInfo]

class SearchResult(BaseModel):
    """Search result with metadata"""
    chunk: ChunkInfo
    score: float
    keyword_score: Optional[float] = None
    semantic_score: Optional[float] = None
