"""
Response Models

Contains all API response models for consistent output formatting.
"""

from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ChunkInfo(BaseModel):
    """Information about a text chunk"""
    id: UUID
    content: str
    document_id: UUID
    chunk_index: int
    similarity_score: Optional[float] = None

class QueryResponse(BaseModel):
    """Response to a query"""
    answer: str
    chunks: List[ChunkInfo]
    processing_time: Optional[float] = None
    confidence_score: Optional[float] = None
    intent: Optional[str] = None

class DocumentInfo(BaseModel):
    """Information about an uploaded document"""
    id: UUID
    filename: str

class UploadResponse(BaseModel):
    """Response to file upload"""
    documents: List[DocumentInfo]
