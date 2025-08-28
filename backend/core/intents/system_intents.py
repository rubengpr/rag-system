"""
System Intents Module

This module handles system management related intents:
- System reset commands
- Memory clearing commands
- Session management commands
- System restart commands
"""

from .base_intent import BaseIntent

class SystemIntents(BaseIntent):
    """Handles system management intents"""
    
    def __init__(self):
        super().__init__()
        self.intent_patterns = self.get_patterns()
        self.intent_priority = ['system_command']
    
    def get_patterns(self) -> dict:
        """Get patterns for system intents"""
        return {
            'system_command': [
                r'\b(reset|restart|reboot|reload|refresh)\b',
                r'\b(clear|wipe|erase|delete)\s+(memory|cache|session|conversation|history)\b',
                r'\b(start\s+over|begin\s+again|new\s+session|fresh\s+start)\b',
                r'\b(forget|ignore|discard)\s+(previous|earlier|past)\b',
                r'\b(restart|reinitialize|rebuild)\s+(system|engine|search)\b'
            ]
        }
    
    def is_simple_intent(self, intent: str) -> bool:
        """System commands are simple intents"""
        return intent == 'system_command'
