"""
Query Processing Module

This module handles query transformation, validation, and security checks.
It includes PII detection, sensitive content filtering, and query optimization.
"""

import re
from typing import Dict

class QueryProcessor:
    """Handles query processing, transformation, and validation"""
    
    def __init__(self):
        # PII detection patterns
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-?\d{2}-?\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
        
        # Medical/legal keywords for refusal
        self.sensitive_keywords = {
            'medical': ['diagnosis', 'treatment', 'symptoms', 'medication', 'doctor', 'patient', 'health'],
            'legal': ['legal advice', 'attorney', 'lawyer', 'contract', 'lawsuit', 'court', 'legal counsel']
        }
        
        # Common acronyms for expansion
        self.acronym_expansions = {
            'ai': 'artificial intelligence',
            'ml': 'machine learning',
            'dl': 'deep learning',
            'api': 'application programming interface',
            'ui': 'user interface',
            'ux': 'user experience'
        }
        
        # Filler words to remove for better search
        self.filler_words = ['what is', 'what are', 'can you', 'please', 'tell me']
    
    def transform_query(self, query: str) -> str:
        """
        Transform query for better retrieval effectiveness
        
        Args:
            query: Original user query
            
        Returns:
            Transformed query optimized for search
        """
        # Remove common filler words that don't help with search
        transformed = query.lower()
        
        for filler in self.filler_words:
            transformed = transformed.replace(filler, ' ').strip()
        
        # Expand common acronyms
        for acronym, expansion in self.acronym_expansions.items():
            # Replace standalone acronyms (word boundaries)
            transformed = re.sub(r'\b' + acronym + r'\b', expansion, transformed)
        
        # Remove excessive whitespace
        transformed = ' '.join(transformed.split())
        
        # If transformation made query too short, use original
        if len(transformed) < 3:
            transformed = query
        
        return transformed
    
    def check_query_refusal(self, query: str) -> str:
        """
        Check if query should be refused due to sensitive content or PII
        
        Args:
            query: User query to check
            
        Returns:
            Refusal reason if query should be refused, empty string otherwise
        """
        query_lower = query.lower()
        
        # Check for PII patterns
        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, query):
                return f"Query contains potential {pii_type.upper()} information"
        
        # Check for medical/legal content
        for category, keywords in self.sensitive_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return f"Query appears to request {category} advice, which I cannot provide"
        
        # Check for other sensitive patterns
        sensitive_patterns = [
            r'\b(personal|private|confidential)\b',
            r'\b(password|secret|security)\b'
        ]
        
        for pattern in sensitive_patterns:
            if re.search(pattern, query_lower):
                return "Query contains potentially sensitive information"
        
        return ""  # No refusal reason
