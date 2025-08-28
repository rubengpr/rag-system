"""
Document Intents Module

This module handles document management related intents:
- Document upload commands
- Document deletion/clearing commands
- Document listing/display commands
- Document management commands
"""

from .base_intent import BaseIntent

class DocumentIntents(BaseIntent):
    """Handles document management intents"""
    
    def __init__(self):
        super().__init__()
        self.intent_patterns = self.get_patterns()
        self.intent_priority = ['document_command']
    
    def get_patterns(self) -> dict:
        """Get patterns for document intents"""
        return {
            'document_command': [
                # Upload commands - must be explicit commands
                r'^\s*(upload|add|import|insert|include)\s+(more|another|additional|new)\s*$',
                r'^\s*(upload|add|import|insert|include)\s+(more|another|additional|new)\s+(document|file|pdf|doc)\s*$',
                
                # Clear/delete commands - must be explicit commands
                r'^\s*(clear|delete|remove|erase|wipe)\s+(all|everything|documents|files)\s*$',
                r'^\s*(clear|delete|remove|erase|wipe)\s+(all|everything)\s*$',
                r'^\s*(clear|delete|remove|erase|wipe)\s+(the\s+)?(documents?|files?|pdfs?|docs?)(\s+i\s+have\s+uploaded)?\s*$',
                
                # Show/list commands - must be explicit commands
                r'^\s*(show|display|list|view|see)\s+(my|all|the)\s+(files|documents|pdfs|docs)\s*$',
                r'^\s*(show|display|list|view|see)\s+(files|documents|pdfs|docs)\s*$',
                
                # Management commands - must be explicit commands
                r'^\s*(manage|organize|sort|arrange)\s+(documents|files|pdfs|docs)\s*$',
                r'^\s*(document|file|pdf|doc)\s+(management|organization|handling)\s*$'
            ]
        }
    
    def is_simple_intent(self, intent: str) -> bool:
        """Document commands are simple intents"""
        return intent == 'document_command'
