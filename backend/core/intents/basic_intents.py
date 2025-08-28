"""
Basic Intents Module

This module handles basic user interaction intents:
- Greeting intents
- Thanks/acknowledgment intents  
- General command intents
"""

from .base_intent import BaseIntent

class BasicIntents(BaseIntent):
    """Handles basic user interaction intents"""
    
    def __init__(self):
        super().__init__()
        self.intent_patterns = self.get_patterns()
        self.intent_priority = ['greeting', 'thanks', 'command']
    
    def get_patterns(self) -> dict:
        """Get patterns for basic intents"""
        return {
            'greeting': [
                r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b',
                r'\b(how are you|howdy|what\'s up)\b'
            ],
            'thanks': [
                r'\b(thank you|thanks|thx|appreciate it|grateful)\b',
                r'\b(that\'s helpful|good answer|well done)\b'
            ],
            'command': [
                r'\b(help|what can you do|explain|describe|tell me about)\b'
            ]
        }
    
    def is_simple_intent(self, intent: str) -> bool:
        """All basic intents are simple intents"""
        return intent in ['greeting', 'thanks', 'command']
