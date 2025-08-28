"""
Modular Intent Detection Module

This module orchestrates intent detection using modular components.
It uses separate classes for different intent categories and coordinates
the detection process with proper priority handling.
"""

import re
from typing import Dict, List, Tuple
from .intents.basic_intents import BasicIntents
from .intents.document_intents import DocumentIntents
from .intents.system_intents import SystemIntents
from .intents.specialized_intents import SpecializedIntents
from .intents.error_intents import ErrorIntents

class IntentDetector:
    """Orchestrates intent detection using modular components"""
    
    def __init__(self):
        # Initialize intent category detectors
        self.error_intents = ErrorIntents()
        self.basic_intents = BasicIntents()
        self.document_intents = DocumentIntents()
        self.system_intents = SystemIntents()
        self.specialized_intents = SpecializedIntents()
        
        # Define detection order (priority order)
        self.intent_categories = [
            self.error_intents,      # Highest priority - handle errors first
            self.basic_intents,      # Basic interactions
            self.document_intents,   # Document management
            self.system_intents,     # System commands
            self.specialized_intents # Specialized processing
        ]
    
    def detect_intent(self, query: str) -> str:
        """
        Detect the intent of a user query using modular components
        
        Args:
            query: User's query text
            
        Returns:
            Intent classification: 'greeting', 'thanks', 'command', 'document_command', 
            'system_command', 'summary_request', 'data_extraction', 'unclear', 
            'out_of_scope', 'question'
        """
        # Check each intent category in priority order
        for intent_category in self.intent_categories:
            matches = intent_category.detect_intents(query)
            if matches:
                # Return the first (highest confidence) match
                return matches[0][0]
        
        # Default to question intent if no matches found
        return 'question'
    
    def is_simple_intent(self, intent: str) -> bool:
        """
        Check if an intent should get a simple response (no RAG processing)
        
        Args:
            intent: Detected intent
            
        Returns:
            True if intent requires simple response, False otherwise
        """
        # Check each category for simple intents
        for intent_category in self.intent_categories:
            if intent_category.is_simple_intent(intent):
                return True
        return False
    
    def is_specialized_intent(self, intent: str) -> bool:
        """
        Check if an intent requires specialized processing
        
        Args:
            intent: Detected intent
            
        Returns:
            True if intent requires specialized processing, False otherwise
        """
        return intent in ['summary_request', 'data_extraction']
    
    def get_all_supported_intents(self) -> List[str]:
        """
        Get all intents supported by the system
        
        Returns:
            List of all supported intent names
        """
        all_intents = []
        for intent_category in self.intent_categories:
            all_intents.extend(intent_category.get_supported_intents())
        return all_intents
