from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# Request Models
class FileUploadRequest(BaseModel):
    """Model for file upload requests"""
    pass

class QueryRequest(BaseModel):
    """Model for query requests"""
    query: str

# Response Models
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

class DocumentInfo(BaseModel):
    """Information about an uploaded document"""
    id: UUID
    filename: str

class UploadResponse(BaseModel):
    """Response to file upload"""
    documents: List[DocumentInfo]

# Internal Models
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
