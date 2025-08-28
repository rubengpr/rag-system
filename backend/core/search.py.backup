"""
Search Module

This module implements custom search algorithms from scratch:
- TF-IDF keyword search using NumPy for efficient vector operations
- Simple semantic search using word overlap
- Result ranking and fusion
"""

from typing import List, Dict, Any, Tuple
from models import ChunkInfo, SearchResult
import numpy as np
import re
from collections import Counter
import math

class SearchEngine:
    """Custom search engine implementing TF-IDF and semantic search from scratch"""
    
    def __init__(self):
        # Core data structures for TF-IDF search
        self.vocabulary = {}  # word -> index mapping
        self.idf_scores = {}  # word -> IDF score
        self.tf_idf_vectors = {}  # chunk_id -> TF-IDF vector
        self.chunks = []  # List of all chunks for search
        
        # Search configuration
        self.min_word_length = 3
        self.max_vocabulary_size = 10000
        
        # Common stop words to filter out
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
            'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
    def preprocess_text(self, text: str) -> List[str]:
        """
        Clean and tokenize text for search processing
        
        Args:
            text: Raw text to process
            
        Returns:
            List of cleaned tokens
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers, keep only letters and spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Split into words and filter
        words = text.split()
        
        # Filter words based on criteria
        filtered_words = []
        for word in words:
            # Remove stop words and short words
            if (len(word) >= self.min_word_length and 
                word not in self.stop_words):
                filtered_words.append(word)
        
        return filtered_words
    
    def calculate_tf(self, words: List[str]) -> Dict[str, float]:
        """
        Calculate Term Frequency for a document
        
        Args:
            words: List of preprocessed words
            
        Returns:
            Dictionary mapping words to their TF scores
        """
        if not words:
            return {}
        
        # Count word occurrences
        word_counts = Counter(words)
        total_words = len(words)
        
        # Calculate TF: frequency of word / total words
        tf_scores = {}
        for word, count in word_counts.items():
            tf_scores[word] = count / total_words
            
        return tf_scores
    
    def calculate_idf(self, documents: List[List[str]]) -> Dict[str, float]:
        """
        Calculate Inverse Document Frequency for vocabulary
        
        Args:
            documents: List of documents, each as list of words
            
        Returns:
            Dictionary mapping words to their IDF scores
        """
        if not documents:
            return {}
        
        total_docs = len(documents)
        idf_scores = {}
        
        # Count documents containing each word
        word_doc_counts = Counter()
        for doc_words in documents:
            # Use set to count unique documents per word
            unique_words = set(doc_words)
            for word in unique_words:
                word_doc_counts[word] += 1
        
        # Calculate IDF: log(total_docs / docs_with_word)
        for word, doc_count in word_doc_counts.items():
            if doc_count > 0:
                idf_scores[word] = math.log(total_docs / doc_count)
            else:
                idf_scores[word] = 0.0
                
        return idf_scores
    
    def build_vocabulary(self, chunks: List[ChunkInfo]) -> Dict[str, int]:
        """
        Build vocabulary from all chunks and assign indices
        
        Args:
            chunks: List of text chunks
            
        Returns:
            Dictionary mapping words to their indices
        """
        # Collect all words from all chunks
        all_words = set()
        for chunk in chunks:
            words = self.preprocess_text(chunk.content)
            all_words.update(words)
        
        # Sort words for consistent indexing
        sorted_words = sorted(all_words)
        
        # Limit vocabulary size if needed
        if len(sorted_words) > self.max_vocabulary_size:
            sorted_words = sorted_words[:self.max_vocabulary_size]
        
        # Create word to index mapping
        vocabulary = {word: idx for idx, word in enumerate(sorted_words)}
        
        return vocabulary
    
    def build_tf_idf_vectors(self, chunks: List[ChunkInfo]):
        """
        Build TF-IDF vectors using NumPy for efficient operations
        
        Args:
            chunks: List of text chunks to index
        """
        self.chunks = chunks
        
        # Build vocabulary
        self.vocabulary = self.build_vocabulary(chunks)
        vocab_size = len(self.vocabulary)
        
        # Prepare documents for IDF calculation
        documents = []
        for chunk in chunks:
            words = self.preprocess_text(chunk.content)
            documents.append(words)
        
        # Calculate IDF scores
        self.idf_scores = self.calculate_idf(documents)
        
        # Build TF-IDF vectors for each chunk
        for chunk in chunks:
            # Get preprocessed words for this chunk
            words = self.preprocess_text(chunk.content)
            
            # Calculate TF scores
            tf_scores = self.calculate_tf(words)
            
            # Create TF-IDF vector
            vector = np.zeros(vocab_size)
            for word, tf_score in tf_scores.items():
                if word in self.vocabulary:
                    idx = self.vocabulary[word]
                    idf_score = self.idf_scores.get(word, 0.0)
                    vector[idx] = tf_score * idf_score
            
            # Store vector for this chunk
            self.tf_idf_vectors[chunk.id] = vector
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity using NumPy for efficiency
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        # Handle zero vectors
        if np.all(vec1 == 0) and np.all(vec2 == 0):
            return 1.0  # Both are zero vectors
        elif np.all(vec1 == 0) or np.all(vec2 == 0):
            return 0.0  # One is zero vector
        
        # Calculate dot product
        dot_product = np.dot(vec1, vec2)
        
        # Calculate vector norms
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        # Avoid division by zero
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        similarity = dot_product / (norm1 * norm2)
        
        # Ensure result is between 0 and 1
        return max(0.0, min(1.0, similarity))
    
    def keyword_search(self, query: str, chunks: List[ChunkInfo], top_k: int = 5) -> List[SearchResult]:
        """
        Perform keyword-based search using TF-IDF with NumPy
        
        Args:
            query: Search query
            chunks: List of chunks to search in
            top_k: Number of top results to return
            
        Returns:
            List of search results sorted by relevance
        """
        if not chunks or not query.strip():
            return []
        
        # Preprocess query
        query_words = self.preprocess_text(query)
        
        if not query_words:
            return []
        
        # Calculate TF scores for query
        query_tf = self.calculate_tf(query_words)
        
        # Create query vector
        vocab_size = len(self.vocabulary)
        query_vector = np.zeros(vocab_size)
        
        for word, tf_score in query_tf.items():
            if word in self.vocabulary:
                idx = self.vocabulary[word]
                idf_score = self.idf_scores.get(word, 0.0)
                query_vector[idx] = tf_score * idf_score
        
        # Calculate similarities with all chunks
        results = []
        for chunk in chunks:
            if chunk.id in self.tf_idf_vectors:
                chunk_vector = self.tf_idf_vectors[chunk.id]
                similarity = self.cosine_similarity(query_vector, chunk_vector)
                
                # Create search result
                search_result = SearchResult(
                    chunk=ChunkInfo(
                        id=chunk.id,
                        content=chunk.content,
                        document_id=chunk.document_id,
                        chunk_index=chunk.chunk_index,
                        similarity_score=similarity
                    ),
                    score=similarity
                )
                results.append(search_result)
        
        # Sort by score (descending) and return top_k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def semantic_search(self, query: str, chunks: List[ChunkInfo], top_k: int = 5) -> List[SearchResult]:
        """
        Perform simple semantic search using word overlap and Jaccard similarity
        
        Args:
            query: Search query
            chunks: List of chunks to search in
            top_k: Number of top results to return
            
        Returns:
            List of search results sorted by relevance
        """
        if not chunks or not query.strip():
            return []
        
        # Preprocess query
        query_words = set(self.preprocess_text(query))
        
        if not query_words:
            return []
        
        # Calculate similarities with all chunks
        results = []
        for chunk in chunks:
            # Preprocess chunk content
            chunk_words = set(self.preprocess_text(chunk.content))
            
            if not chunk_words:
                continue
            
            # Calculate Jaccard similarity
            intersection = len(query_words & chunk_words)
            union = len(query_words | chunk_words)
            
            if union == 0:
                similarity = 0.0
            else:
                similarity = intersection / union
            
            # Boost exact word matches
            exact_matches = len(query_words & chunk_words)
            if exact_matches > 0:
                similarity += exact_matches * 0.1  # Small boost for exact matches
            
            # Cap similarity at 1.0
            similarity = min(1.0, similarity)
            
            # Create search result
            search_result = SearchResult(
                chunk=ChunkInfo(
                    id=chunk.id,
                    content=chunk.content,
                    document_id=chunk.document_id,
                    chunk_index=chunk.chunk_index,
                    similarity_score=similarity
                ),
                score=similarity
            )
            results.append(search_result)
        
        # Sort by score (descending) and return top_k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def hybrid_search(self, query: str, chunks: List[ChunkInfo], top_k: int = 5) -> List[SearchResult]:
        """
        Combine keyword and semantic search results with weighted fusion
        
        Args:
            query: Search query
            chunks: List of chunks to search in
            top_k: Number of top results to return
            
        Returns:
            List of search results sorted by relevance
        """
        # Get results from both search methods
        keyword_results = self.keyword_search(query, chunks, top_k * 2)
        semantic_results = self.semantic_search(query, chunks, top_k * 2)
        
        # Create a mapping of chunk_id to combined scores
        combined_scores = {}
        
        # Process keyword results (70% weight)
        for result in keyword_results:
            chunk_id = result.chunk.id
            combined_scores[chunk_id] = {
                'score': result.score * 0.7,
                'chunk': result.chunk,
                'keyword_score': result.score,
                'semantic_score': 0.0
            }
        
        # Process semantic results (30% weight)
        for result in semantic_results:
            chunk_id = result.chunk.id
            if chunk_id in combined_scores:
                # Add semantic score to existing entry
                combined_scores[chunk_id]['score'] += result.score * 0.3
                combined_scores[chunk_id]['semantic_score'] = result.score
            else:
                # Create new entry
                combined_scores[chunk_id] = {
                    'score': result.score * 0.3,
                    'chunk': result.chunk,
                    'keyword_score': 0.0,
                    'semantic_score': result.score
                }
        
        # Convert to SearchResult objects
        results = []
        for chunk_id, data in combined_scores.items():
            # Update chunk with combined similarity score
            chunk = ChunkInfo(
                id=data['chunk'].id,
                content=data['chunk'].content,
                document_id=data['chunk'].document_id,
                chunk_index=data['chunk'].chunk_index,
                similarity_score=data['score']
            )
            
            search_result = SearchResult(chunk=chunk, score=data['score'])
            results.append(search_result)
        
        # Sort by combined score and return top_k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def rank_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        Re-rank search results for better relevance
        
        Args:
            results: List of search results to re-rank
            
        Returns:
            Re-ranked list of search results
        """

        if not results:
            return results
        
        for i, result in enumerate(results):
            # Check if result has keyword_score attribute
            has_keyword_score = hasattr(result, 'keyword_score')
            
            # Boost high-scoring keyword matches
            if hasattr(result, 'keyword_score') and result.keyword_score is not None and result.keyword_score > 0.8:
                result.score += 0.1
            
            # Penalize very short chunks
            content_length = len(result.chunk.content.strip())
            if content_length < 50:
                result.score -= 0.1
            elif content_length > 500:
                result.score += 0.05  # Slight boost for longer chunks
        
        # Re-sort by adjusted scores
        results.sort(key=lambda x: x.score, reverse=True)
        return results
