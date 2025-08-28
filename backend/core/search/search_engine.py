"""
Main Search Engine Module

Orchestrates all search components and provides a unified interface for search operations.
"""

from typing import List, Dict, Any
from .base_search import BaseSearchEngine
from .tfidf_search import TFIDFSearch
from .semantic_search import SemanticSearch
from .ranker import SearchRanker
from .preprocessing import TextPreprocessor
from models import ChunkInfo, SearchResult

class SearchEngine(BaseSearchEngine):
    """Main search engine that orchestrates TF-IDF, semantic search, and ranking"""
    
    def __init__(self):
        # Initialize components
        self.preprocessor = TextPreprocessor()
        self.tfidf_search = TFIDFSearch(self.preprocessor)
        self.semantic_search = SemanticSearch(self.preprocessor)
        self.ranker = SearchRanker()
        
        # Store chunks for reference
        self.chunks = []
    
    def build_index(self, chunks: List[ChunkInfo]) -> None:
        """
        Build search index from chunks
        
        Args:
            chunks: List of chunks to index
        """
        self.chunks = chunks
        
        # Build TF-IDF index
        self.tfidf_search.build_tf_idf_vectors(chunks)
        
        # Build semantic index
        self.semantic_search.build_semantic_index(chunks)
    
    def search(self, query: str, top_k: int = 5, threshold: float = 0.1) -> List[SearchResult]:
        """
        Search for relevant chunks given a query
        
        Args:
            query: Search query
            top_k: Number of top results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of search results
        """
        if not self.chunks:
            return []
        
        # Perform TF-IDF search
        tfidf_results = self.tfidf_search.search(query, top_k=top_k * 2)
        
        # Perform semantic search
        semantic_results = self.semantic_search.search(query, top_k=top_k * 2)
        
        # Fuse results
        fused_results = self.ranker.fuse_results(tfidf_results, semantic_results)
        
        # Apply threshold filtering
        filtered_results = self.ranker.filter_by_threshold(fused_results, threshold)
        
        # Re-rank results
        reranked_results = self.ranker.rank_results(filtered_results, self.chunks, query)
        
        # Limit results
        final_results = self.ranker.limit_results(reranked_results, top_k)
        
        # Convert to SearchResult objects
        return self.ranker.create_search_results(final_results, self.chunks)
    
    def add_chunks(self, chunks: List[ChunkInfo]) -> None:
        """
        Add new chunks to the existing index
        
        Args:
            chunks: New chunks to add
        """
        # Add to existing chunks
        self.chunks.extend(chunks)
        
        # Rebuild indices with all chunks
        self.build_index(self.chunks)
    
    def clear_index(self) -> None:
        """Clear all indexed data"""
        self.chunks = []
        self.tfidf_search.chunks = []
        self.tfidf_search.tf_idf_vectors = {}
        self.tfidf_search.vocabulary = {}
        self.tfidf_search.idf_scores = {}
        self.semantic_search.chunks = []
        self.semantic_search.chunk_words = {}
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the current index
        
        Returns:
            Dictionary with index statistics
        """
        tfidf_stats = self.tfidf_search.get_vocabulary_stats()
        semantic_stats = self.semantic_search.get_search_stats()
        
        return {
            'total_chunks': len(self.chunks),
            'tfidf': tfidf_stats,
            'semantic': semantic_stats
        }
    
    def search_tfidf_only(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        Search using only TF-IDF algorithm
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of search results
        """
        tfidf_results = self.tfidf_search.search(query, top_k)
        return self.ranker.create_search_results(tfidf_results, self.chunks)
    
    def search_semantic_only(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        Search using only semantic search
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of search results
        """
        semantic_results = self.semantic_search.search(query, top_k)
        return self.ranker.create_search_results(semantic_results, self.chunks)
    
    def get_chunk_keywords(self, chunk_id: str) -> List[str]:
        """
        Get important keywords from a specific chunk
        
        Args:
            chunk_id: ID of the chunk
            
        Returns:
            List of important keywords
        """
        return self.semantic_search.get_chunk_keywords(chunk_id)
    
    def preprocess_query(self, query: str) -> List[str]:
        """
        Preprocess a query for search
        
        Args:
            query: Raw query text
            
        Returns:
            List of preprocessed tokens
        """
        return self.preprocessor.preprocess_text(query)
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text: Input text
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of important keywords
        """
        return self.preprocessor.extract_keywords(text, max_keywords)
