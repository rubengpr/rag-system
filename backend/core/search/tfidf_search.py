"""
TF-IDF Search Module

Implements TF-IDF (Term Frequency-Inverse Document Frequency) search algorithm.
"""

from typing import List, Dict, Tuple
from collections import Counter
import numpy as np
import math
from .preprocessing import TextPreprocessor
from models import ChunkInfo

class TFIDFSearch:
    """TF-IDF search implementation"""
    
    def __init__(self, preprocessor: TextPreprocessor):
        self.preprocessor = preprocessor
        
        # Core data structures for TF-IDF search
        self.vocabulary = {}  # word -> index mapping
        self.idf_scores = {}  # word -> IDF score
        self.tf_idf_vectors = {}  # chunk_id -> TF-IDF vector
        self.chunks = []  # List of all chunks for search
    
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
        
        # Count documents containing each word
        doc_count = Counter()
        total_docs = len(documents)
        
        for doc in documents:
            unique_words = set(doc)
            for word in unique_words:
                doc_count[word] += 1
        
        # Calculate IDF: log(total_docs / docs_containing_word)
        idf_scores = {}
        for word, count in doc_count.items():
            idf_scores[word] = math.log(total_docs / count)
            
        return idf_scores
    
    def build_vocabulary(self, chunks: List[ChunkInfo]) -> None:
        """
        Build vocabulary from all chunks
        
        Args:
            chunks: List of chunks to process
        """
        # Process all chunks to extract words
        all_words = set()
        for chunk in chunks:
            words = self.preprocessor.preprocess_text(chunk.content)
            all_words.update(words)
        
        # Build vocabulary mapping (word -> index)
        self.vocabulary = {word: idx for idx, word in enumerate(sorted(all_words))}
        
        # Limit vocabulary size if needed
        if len(self.vocabulary) > self.preprocessor.max_vocabulary_size:
            # Keep most common words (simplified approach)
            word_counts = Counter()
            for chunk in chunks:
                words = self.preprocessor.preprocess_text(chunk.content)
                word_counts.update(words)
            
            # Get top words by frequency
            top_words = [word for word, count in word_counts.most_common(self.preprocessor.max_vocabulary_size)]
            self.vocabulary = {word: idx for idx, word in enumerate(top_words)}
    
    def build_tf_idf_vectors(self, chunks: List[ChunkInfo]) -> None:
        """
        Build TF-IDF vectors for all chunks
        
        Args:
            chunks: List of chunks to process
        """
        self.chunks = chunks
        
        # Build vocabulary first
        self.build_vocabulary(chunks)
        
        # Prepare documents for IDF calculation
        documents = []
        for chunk in chunks:
            words = self.preprocessor.preprocess_text(chunk.content)
            documents.append(words)
        
        # Calculate IDF scores
        self.idf_scores = self.calculate_idf(documents)
        
        # Calculate TF-IDF vectors for each chunk
        vocab_size = len(self.vocabulary)
        for chunk in chunks:
            words = self.preprocessor.preprocess_text(chunk.content)
            tf_scores = self.calculate_tf(words)
            
            # Create TF-IDF vector
            tf_idf_vector = np.zeros(vocab_size)
            
            for word, tf_score in tf_scores.items():
                if word in self.vocabulary and word in self.idf_scores:
                    word_idx = self.vocabulary[word]
                    tf_idf_vector[word_idx] = tf_score * self.idf_scores[word]
            
            self.tf_idf_vectors[chunk.id] = tf_idf_vector
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Search for relevant chunks using TF-IDF
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of (chunk_id, score) tuples
        """
        if not self.chunks or not self.tf_idf_vectors:
            return []
        
        # Preprocess query
        query_words = self.preprocessor.preprocess_text(query)
        
        if not query_words:
            return []
        
        # Calculate query TF-IDF vector
        query_tf_scores = self.calculate_tf(query_words)
        vocab_size = len(self.vocabulary)
        query_vector = np.zeros(vocab_size)
        
        for word, tf_score in query_tf_scores.items():
            if word in self.vocabulary and word in self.idf_scores:
                word_idx = self.vocabulary[word]
                query_vector[word_idx] = tf_score * self.idf_scores[word]
        
        # Calculate cosine similarity with all chunks
        similarities = []
        for chunk in self.chunks:
            if chunk.id in self.tf_idf_vectors:
                chunk_vector = self.tf_idf_vectors[chunk.id]
                
                # Calculate cosine similarity
                similarity = self._cosine_similarity(query_vector, chunk_vector)
                similarities.append((chunk.id, similarity))
        
        # Sort by similarity and return top_k results
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def get_vocabulary_stats(self) -> Dict[str, int]:
        """Get vocabulary statistics"""
        return {
            'vocabulary_size': len(self.vocabulary),
            'chunks_count': len(self.chunks),
            'vectors_count': len(self.tf_idf_vectors)
        }
