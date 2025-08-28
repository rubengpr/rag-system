"""
Text Preprocessing Module

Handles text cleaning, tokenization, and normalization for search processing.
"""

import re
from typing import List, Set

class TextPreprocessor:
    """Handles text preprocessing for search algorithms"""
    
    def __init__(self):
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
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text: Input text
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of important keywords
        """
        words = self.preprocess_text(text)
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text for consistent processing
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
