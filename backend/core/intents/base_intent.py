"""
Base Intent Class

This module provides the base class for all intent detection classes.
It includes common functionality and interfaces.
"""

import re
from typing import List, Tuple, Dict, Optional
from abc import ABC, abstractmethod

class BaseIntent(ABC):
    """Base class for all intent detection classes"""
    
    def __init__(self):
        self.intent_patterns: Dict[str, List[str]] = {}
        self.intent_priority: List[str] = []
    
    @abstractmethod
    def get_patterns(self) -> Dict[str, List[str]]:
        """
        Get the patterns for this intent category
        
        Returns:
            Dictionary mapping intent names to pattern lists
        """
        pass
    
    def detect_intents(self, query: str) -> List[Tuple[str, float]]:
        """
        Detect all matching intents in the query with confidence scores
        
        Args:
            query: User query text
            
        Returns:
            List of (intent_name, confidence_score) tuples
        """
        query_lower = query.lower().strip()
        matches = []
        
        for intent_name, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    # Calculate confidence based on pattern match
                    confidence = self._calculate_confidence(pattern, query_lower)
                    matches.append((intent_name, confidence))
                    break  # Only use first match per intent
        
        return matches
    
    def _calculate_confidence(self, pattern: str, query: str) -> float:
        """
        Calculate confidence score for a pattern match
        
        Args:
            pattern: The regex pattern that matched
            query: The query text
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Base confidence
        confidence = 0.8
        
        # Higher confidence for exact word matches
        if pattern.startswith(r'\b') and pattern.endswith(r'\b'):
            confidence += 0.1
        
        # Higher confidence for start-of-sentence patterns
        if pattern.startswith(r'^\s*'):
            confidence += 0.1
        
        # Cap at 1.0
        return min(confidence, 1.0)
    
    def get_supported_intents(self) -> List[str]:
        """
        Get list of intents supported by this class
        
        Returns:
            List of intent names
        """
        return list(self.intent_patterns.keys())
    
    def is_simple_intent(self, intent: str) -> bool:
        """
        Check if an intent should get a simple response
        
        Args:
            intent: Intent name
            
        Returns:
            True if intent requires simple response
        """
        return False  # Override in subclasses for simple intents
