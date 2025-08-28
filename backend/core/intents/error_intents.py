"""
Error Intents Module

This module handles error and edge case intents:
- Unclear/confused queries
- Out-of-scope requests
- Other error scenarios
"""

from .base_intent import BaseIntent

class ErrorIntents(BaseIntent):
    """Handles error and edge case intents"""
    
    def __init__(self):
        super().__init__()
        self.intent_patterns = self.get_patterns()
        self.intent_priority = ['unclear', 'out_of_scope']
    
    def get_patterns(self) -> dict:
        """Get patterns for error intents"""
        return {
            'unclear': [
                r'\?\?\?',  # Multiple question marks
                r'\b(hmm|huh|um|uh|err|umm)\b',  # Hesitation sounds
                r'\b(i don\'t know|idk|not sure|confused|unclear)\b',  # Uncertainty
                r'\b(what do you mean|i don\'t understand|can you explain)\b',  # Clarification requests
                r'^\s*$',  # Empty or whitespace-only queries
                r'^\s*[^\w\s]*\s*$'  # Only special characters
            ],
            'out_of_scope': [
                r'\b(weather|temperature|forecast|rain|sunny)\b',  # Weather queries
                r'\b(joke|funny|humor|laugh|entertain)\b',  # Entertainment
                r'\b(calculate|math|addition|subtraction|multiplication|division)\b',  # Math
                r'\b(time|date|clock|calendar|schedule)\b',  # Time/date
                r'\b(translate|language|spanish|french|german)\b',  # Translation
                r'\b(news|politics|sports|celebrity|gossip)\b',  # General news
                r'\b(recipe|cooking|food|restaurant|menu)\b',  # Food/cooking
                r'\b(music|song|artist|album|playlist)\b'  # Music
            ]
        }
    
    def is_simple_intent(self, intent: str) -> bool:
        """Error intents are simple intents"""
        return intent in ['unclear', 'out_of_scope']
