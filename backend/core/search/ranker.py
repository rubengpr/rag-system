"""
Search Ranker Module

Handles result ranking, fusion, and re-ranking of search results.
"""

from typing import List, Dict, Tuple
from models import SearchResult, ChunkInfo

class SearchRanker:
    """Handles ranking and fusion of search results"""
    
    def __init__(self):
        # Ranking weights for hybrid search
        self.tfidf_weight = 0.7
        self.semantic_weight = 0.3
        
        # Re-ranking parameters
        self.keyword_boost = 1.2
        self.exact_match_boost = 1.5
        self.position_penalty = 0.1
    
    def fuse_results(self, 
                    tfidf_results: List[Tuple[str, float]], 
                    semantic_results: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """
        Fuse TF-IDF and semantic search results
        
        Args:
            tfidf_results: TF-IDF search results
            semantic_results: Semantic search results
            
        Returns:
            Fused results with hybrid scores
        """
        # Create score dictionaries for easy lookup
        tfidf_scores = dict(tfidf_results)
        semantic_scores = dict(semantic_results)
        
        # Get all unique chunk IDs
        all_chunk_ids = set(tfidf_scores.keys()) | set(semantic_scores.keys())
        
        # Calculate hybrid scores
        hybrid_results = []
        for chunk_id in all_chunk_ids:
            tfidf_score = tfidf_scores.get(chunk_id, 0.0)
            semantic_score = semantic_scores.get(chunk_id, 0.0)
            
            # Weighted combination
            hybrid_score = (self.tfidf_weight * tfidf_score + 
                          self.semantic_weight * semantic_score)
            
            hybrid_results.append((chunk_id, hybrid_score))
        
        # Sort by hybrid score
        hybrid_results.sort(key=lambda x: x[1], reverse=True)
        return hybrid_results
    
    def rank_results(self, 
                    results: List[Tuple[str, float]], 
                    chunks: List[ChunkInfo],
                    query: str) -> List[Tuple[str, float]]:
        """
        Re-rank results based on additional factors
        
        Args:
            results: Initial search results
            chunks: All available chunks
            query: Original search query
            
        Returns:
            Re-ranked results
        """
        if not results:
            return []
        
        # Create chunk lookup
        chunk_lookup = {chunk.id: chunk for chunk in chunks}
        
        # Apply re-ranking adjustments
        reranked_results = []
        for i, (chunk_id, score) in enumerate(results):
            chunk = chunk_lookup.get(chunk_id)
            if not chunk:
                continue
            
            # Start with original score
            adjusted_score = score
            
            # Apply keyword boost
            keyword_boost = self._calculate_keyword_boost(chunk.content, query)
            adjusted_score *= keyword_boost
            
            # Apply exact match boost
            exact_match_boost = self._calculate_exact_match_boost(chunk.content, query)
            adjusted_score *= exact_match_boost
            
            # Apply position penalty (later results get slight penalty)
            position_penalty = 1.0 - (i * self.position_penalty)
            adjusted_score *= position_penalty
            
            reranked_results.append((chunk_id, adjusted_score))
        
        # Sort by adjusted scores
        reranked_results.sort(key=lambda x: x[1], reverse=True)
        return reranked_results
    
    def _calculate_keyword_boost(self, content: str, query: str) -> float:
        """
        Calculate keyword boost based on query terms in content
        
        Args:
            content: Chunk content
            query: Search query
            
        Returns:
            Boost multiplier
        """
        content_lower = content.lower()
        query_lower = query.lower()
        
        # Count query words in content
        query_words = query_lower.split()
        matches = sum(1 for word in query_words if word in content_lower)
        
        if matches == 0:
            return 1.0
        
        # Boost based on number of matches
        return self.keyword_boost ** matches
    
    def _calculate_exact_match_boost(self, content: str, query: str) -> float:
        """
        Calculate exact match boost for query phrases
        
        Args:
            content: Chunk content
            query: Search query
            
        Returns:
            Boost multiplier
        """
        content_lower = content.lower()
        query_lower = query.lower()
        
        # Check for exact phrase match
        if query_lower in content_lower:
            return self.exact_match_boost
        
        return 1.0
    
    def filter_by_threshold(self, 
                          results: List[Tuple[str, float]], 
                          threshold: float = 0.1) -> List[Tuple[str, float]]:
        """
        Filter results by similarity threshold
        
        Args:
            results: Search results
            threshold: Minimum similarity threshold
            
        Returns:
            Filtered results
        """
        return [(chunk_id, score) for chunk_id, score in results if score >= threshold]
    
    def limit_results(self, 
                     results: List[Tuple[str, float]], 
                     max_results: int = 5) -> List[Tuple[str, float]]:
        """
        Limit number of results
        
        Args:
            results: Search results
            max_results: Maximum number of results
            
        Returns:
            Limited results
        """
        return results[:max_results]
    
    def create_search_results(self, 
                            ranked_results: List[Tuple[str, float]], 
                            chunks: List[ChunkInfo]) -> List[SearchResult]:
        """
        Convert ranked results to SearchResult objects
        
        Args:
            ranked_results: Ranked search results
            chunks: All available chunks
            
        Returns:
            List of SearchResult objects
        """
        chunk_lookup = {chunk.id: chunk for chunk in chunks}
        search_results = []
        
        for chunk_id, score in ranked_results:
            chunk = chunk_lookup.get(chunk_id)
            if chunk:
                search_result = SearchResult(
                    chunk=chunk,
                    score=score
                )
                search_results.append(search_result)
        
        return search_results
