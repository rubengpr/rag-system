"""
Semantic Search Module

Implements semantic search using word overlap and Jaccard similarity.
"""

from typing import List, Dict, Tuple, Set
from .preprocessing import TextPreprocessor
from models import ChunkInfo

class SemanticSearch:
    """Semantic search implementation using word overlap and Jaccard similarity"""
    
    def __init__(self, preprocessor: TextPreprocessor):
        self.preprocessor = preprocessor
        self.chunks = []  # List of all chunks for search
        self.chunk_words = {}  # chunk_id -> set of words
    
    def build_semantic_index(self, chunks: List[ChunkInfo]) -> None:
        """
        Build semantic search index from chunks
        
        Args:
            chunks: List of chunks to process
        """
        self.chunks = chunks
        self.chunk_words = {}
        
        # Preprocess all chunks and store word sets
        for chunk in chunks:
            words = self.preprocessor.preprocess_text(chunk.content)
            self.chunk_words[chunk.id] = set(words)
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for relevant chunks using semantic similarity
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of (chunk_id, score) tuples
        """
        if not self.chunks or not self.chunk_words:
            return []
        
        # Preprocess query
        query_words = set(self.preprocessor.preprocess_text(query))
        
        if not query_words:
            return []
        
        # Calculate similarities with all chunks
        similarities = []
        for chunk in self.chunks:
            if chunk.id in self.chunk_words:
                chunk_words = self.chunk_words[chunk.id]
                
                # Calculate Jaccard similarity
                similarity = self._jaccard_similarity(query_words, chunk_words)
                similarities.append((chunk.id, similarity))
        
        # Sort by similarity and return top_k results
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def _jaccard_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """
        Calculate Jaccard similarity between two sets
        
        Args:
            set1: First set of words
            set2: Second set of words
            
        Returns:
            Jaccard similarity score
        """
        if not set1 or not set2:
            return 0.0
        
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        return len(intersection) / len(union)
    
    def _word_overlap_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """
        Calculate word overlap similarity (intersection size)
        
        Args:
            set1: First set of words
            set2: Second set of words
            
        Returns:
            Word overlap similarity score
        """
        if not set1 or not set2:
            return 0.0
        
        intersection = set1.intersection(set2)
        return len(intersection)
    
    def search_with_overlap(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search using word overlap similarity
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of (chunk_id, score) tuples
        """
        if not self.chunks or not self.chunk_words:
            return []
        
        # Preprocess query
        query_words = set(self.preprocessor.preprocess_text(query))
        
        if not query_words:
            return []
        
        # Calculate word overlap with all chunks
        similarities = []
        for chunk in self.chunks:
            if chunk.id in self.chunk_words:
                chunk_words = self.chunk_words[chunk.id]
                
                # Calculate word overlap similarity
                similarity = self._word_overlap_similarity(query_words, chunk_words)
                similarities.append((chunk.id, similarity))
        
        # Sort by similarity and return top_k results
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def get_chunk_keywords(self, chunk_id: str, max_keywords: int = 10) -> List[str]:
        """
        Get important keywords from a chunk
        
        Args:
            chunk_id: ID of the chunk
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of important keywords
        """
        if chunk_id not in self.chunk_words:
            return []
        
        words = list(self.chunk_words[chunk_id])
        
        # Simple keyword extraction: return most frequent words
        # In a more sophisticated implementation, you could use TF-IDF scores
        return words[:max_keywords]
    
    def get_search_stats(self) -> Dict[str, int]:
        """Get search statistics"""
        return {
            'chunks_count': len(self.chunks),
            'indexed_chunks': len(self.chunk_words),
            'avg_words_per_chunk': sum(len(words) for words in self.chunk_words.values()) / len(self.chunk_words) if self.chunk_words else 0
        }
