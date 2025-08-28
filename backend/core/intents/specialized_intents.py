"""
Specialized Intents Module

This module handles specialized processing intents:
- Summary request intents
- Data extraction intents
- Other specialized analysis intents
"""

from .base_intent import BaseIntent

class SpecializedIntents(BaseIntent):
    """Handles specialized processing intents"""
    
    def __init__(self):
        super().__init__()
        self.intent_patterns = self.get_patterns()
        self.intent_priority = ['summary_request', 'data_extraction']
    
    def get_patterns(self) -> dict:
        """Get patterns for specialized intents"""
        return {
            'summary_request': [
                r'\b(summarize|summary|summarise|summarization)\b',
                r'\b(give\s+me\s+a?\s+summary|provide\s+a?\s+summary|create\s+a?\s+summary)\b',
                r'\b(brief\s+overview|quick\s+overview|short\s+overview)\b',
                r'\b(tl;?dr|tldr|too\s+long\s+didn\'t\s+read)\b',
                r'\b(condense|condensed|abbreviated|short\s+version)\b',
                r'\b(key\s+points|main\s+points|essential\s+points)\b',
                r'\b(overview|synopsis|abstract|gist)\b'
            ],
            'data_extraction': [
                r'\b(extract|extraction|extracted)\b',
                r'\b(list\s+all|show\s+all|display\s+all|get\s+all)\b',
                r'\b(what\s+are\s+the|what\s+is\s+the|give\s+me\s+the)\b',
                r'\b(find\s+all|search\s+for\s+all|locate\s+all)\b',
                r'\b(compile|gather|collect|assemble)\s+(all|every|each)\b',
                r'\b(table|list|chart|inventory|catalog)\s+(of|with|containing)\b',
                r'\b(organize|structure|format)\s+(as|into|in)\s+(list|table|chart)\b'
            ]
        }
    
    def is_simple_intent(self, intent: str) -> bool:
        """Specialized intents require custom processing"""
        return False  # These require specialized handling
