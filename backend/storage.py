"""
In-Memory Storage Management

This module handles all in-memory storage operations for documents and chunks.
Provides a clean interface for storage operations and maintains data consistency.
"""

from typing import Dict, List, Optional
import logging
from models import DocumentInfo, ChunkInfo

logger = logging.getLogger(__name__)

class DocumentStorage:
    """Manages in-memory storage for documents and chunks"""
    
    def __init__(self):
        self._documents: Dict[str, dict] = {}  # document_id -> document_info
        self._chunks: Dict[str, List[dict]] = {}  # document_id -> list of chunks
        self._all_chunks: List[dict] = []  # List of all chunks for search engine
        
    def add_document(self, document_id: str, document_info: dict) -> None:
        """Add a document to storage"""
        self._documents[document_id] = document_info
        logger.info(f"Added document {document_id} to storage")
        
    def add_chunks(self, document_id: str, chunks: List[dict]) -> None:
        """Add chunks for a document to storage"""
        self._chunks[document_id] = chunks
        self._all_chunks.extend(chunks)
        logger.info(f"Added {len(chunks)} chunks for document {document_id}")
        
    def get_document(self, document_id: str) -> Optional[dict]:
        """Get document information by ID"""
        return self._documents.get(document_id)
        
    def get_chunks(self, document_id: str) -> List[dict]:
        """Get chunks for a specific document"""
        return self._chunks.get(document_id, [])
        
    def get_all_chunks(self) -> List[dict]:
        """Get all chunks for search engine initialization"""
        return self._all_chunks.copy()
        
    def get_all_documents(self) -> List[DocumentInfo]:
        """Get all documents as DocumentInfo objects"""
        documents = []
        for doc_id, doc_info in self._documents.items():
            document = DocumentInfo(
                id=doc_id,
                filename=doc_info["filename"]
            )
            documents.append(document)
        return documents
        
    def clear_all(self) -> None:
        """Clear all stored documents and chunks"""
        self._documents.clear()
        self._chunks.clear()
        self._all_chunks.clear()
        logger.info("Cleared all documents and chunks from storage")
        
    def get_document_count(self) -> int:
        """Get the number of stored documents"""
        return len(self._documents)
        
    def get_chunk_count(self) -> int:
        """Get the total number of chunks"""
        return len(self._all_chunks)
        
    def get_storage_stats(self) -> dict:
        """Get storage statistics"""
        return {
            "document_count": self.get_document_count(),
            "chunk_count": self.get_chunk_count(),
            "documents": list(self._documents.keys())
        }

# Global storage instance
storage = DocumentStorage()
