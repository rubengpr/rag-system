"""
Base Search Interface

Defines the abstract interface for search implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from models import ChunkInfo, SearchResult

class BaseSearchEngine(ABC):
    """Abstract base class for search engine implementations"""
    
    @abstractmethod
    def build_index(self, chunks: List[ChunkInfo]) -> None:
        """Build search index from chunks"""
        pass
    
    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search for relevant chunks given a query"""
        pass
    
    @abstractmethod
    def add_chunks(self, chunks: List[ChunkInfo]) -> None:
        """Add new chunks to the existing index"""
        pass
    
    @abstractmethod
    def clear_index(self) -> None:
        """Clear all indexed data"""
        pass
    
    @abstractmethod
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the current index"""
        pass
