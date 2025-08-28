"""
Search Module Package

This package implements custom search algorithms from scratch:
- TF-IDF keyword search using NumPy for efficient vector operations
- Simple semantic search using word overlap
- Result ranking and fusion
"""

from .base_search import BaseSearchEngine
from .search_engine import SearchEngine
from .tfidf_search import TFIDFSearch
from .semantic_search import SemanticSearch
from .ranker import SearchRanker
from .preprocessing import TextPreprocessor

__all__ = [
    'BaseSearchEngine',
    'SearchEngine',
    'TFIDFSearch',
    'SemanticSearch', 
    'SearchRanker',
    'TextPreprocessor'
]
