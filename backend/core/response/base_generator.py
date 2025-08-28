"""
Base Response Generator

Provides common functionality and interfaces for all response generators.
"""

from abc import ABC, abstractmethod
from typing import List
from models import QueryRequest, QueryResponse, ChunkInfo
from ..llm import MistralClient
from ..search import SearchEngine

class BaseResponseGenerator(ABC):
    """Base class for all response generators"""
    
    def __init__(self, llm_client: MistralClient, search_engine: SearchEngine):
        self.llm_client = llm_client
        self.search_engine = search_engine
    
    def check_documents_available(self) -> bool:
        """Check if documents are available for processing"""
        return len(self.search_engine.chunks) > 0
    
    def check_search_engine_initialized(self) -> bool:
        """Check if search engine is properly initialized"""
        return self.search_engine.tf_idf_vectors is not None and len(self.search_engine.tf_idf_vectors) > 0
    
    def get_available_chunks(self, limit: int = 10) -> List[ChunkInfo]:
        """Get available chunks for processing"""
        if not self.check_documents_available():
            return []
        return self.search_engine.chunks[:limit]
    
    def format_context_from_chunks(self, chunks: List[ChunkInfo]) -> str:
        """Format chunks into context string"""
        if not chunks:
            return ""
        return "\n\n".join([f"Document {chunk.document_id}: {chunk.content}" for chunk in chunks])
    
    def create_error_response(self, message: str, intent: str = "error") -> QueryResponse:
        """Create a standardized error response"""
        return QueryResponse(
            answer=message,
            chunks=[],
            processing_time=0.0,
            confidence_score=0.0,
            intent=intent
        )
    
    @abstractmethod
    def generate_response(self, request: QueryRequest) -> QueryResponse:
        """Generate response for the given request"""
        pass
