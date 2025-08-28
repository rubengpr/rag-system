"""
Intent Detection Module

This module handles the detection and classification of user query intents.
It uses pattern matching to categorize queries into different types.
"""

import re
from typing import Dict, List

class IntentDetector:
    """Handles intent detection for user queries"""
    
    def __init__(self):
        # Basic intent patterns
        self.greeting_patterns = [
            r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b',
            r'\b(how are you|howdy|what\'s up)\b'
        ]
        
        self.thanks_patterns = [
            r'\b(thank you|thanks|thx|appreciate it|grateful)\b',
            r'\b(that\'s helpful|good answer|well done)\b'
        ]
        
        self.command_patterns = [
            r'\b(help|what can you do|explain|describe|tell me about)\b'
        ]
        
        # Document management command patterns
        self.document_command_patterns = [
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
        
        # System command patterns
        self.system_command_patterns = [
            r'\b(reset|restart|reboot|reload|refresh)\b',
            r'\b(clear|wipe|erase|delete)\s+(memory|cache|session|conversation|history)\b',
            r'\b(start\s+over|begin\s+again|new\s+session|fresh\s+start)\b',
            r'\b(forget|ignore|discard)\s+(previous|earlier|past)\b',
            r'\b(restart|reinitialize|rebuild)\s+(system|engine|search)\b'
        ]
        
        # Summary request patterns
        self.summary_patterns = [
            r'\b(summarize|summary|summarise|summarization)\b',
            r'\b(give\s+me\s+a?\s+summary|provide\s+a?\s+summary|create\s+a?\s+summary)\b',
            r'\b(brief\s+overview|quick\s+overview|short\s+overview)\b',
            r'\b(tl;?dr|tldr|too\s+long\s+didn\'t\s+read)\b',
            r'\b(condense|condensed|abbreviated|short\s+version)\b',
            r'\b(key\s+points|main\s+points|essential\s+points)\b',
            r'\b(overview|synopsis|abstract|gist)\b'
        ]
        
        # Data extraction patterns
        self.data_extraction_patterns = [
            r'\b(extract|extraction|extracted)\b',
            r'\b(list\s+all|show\s+all|display\s+all|get\s+all)\b',
            r'\b(what\s+are\s+the|what\s+is\s+the|give\s+me\s+the)\b',
            r'\b(find\s+all|search\s+for\s+all|locate\s+all)\b',
            r'\b(compile|gather|collect|assemble)\s+(all|every|each)\b',
            r'\b(table|list|chart|inventory|catalog)\s+(of|with|containing)\b',
            r'\b(organize|structure|format)\s+(as|into|in)\s+(list|table|chart)\b'
        ]
        
        # Error and edge case intent patterns
        self.unclear_patterns = [
            r'\?\?\?',  # Multiple question marks
            r'\b(hmm|huh|um|uh|err|umm)\b',  # Hesitation sounds
            r'\b(i don\'t know|idk|not sure|confused|unclear)\b',  # Uncertainty
            r'\b(what do you mean|i don\'t understand|can you explain)\b',  # Clarification requests
            r'^\s*$',  # Empty or whitespace-only queries
            r'^\s*[^\w\s]*\s*$'  # Only special characters
        ]
        
        self.out_of_scope_patterns = [
            r'\b(weather|temperature|forecast|rain|sunny)\b',  # Weather queries
            r'\b(joke|funny|humor|laugh|entertain)\b',  # Entertainment
            r'\b(calculate|math|addition|subtraction|multiplication|division)\b',  # Math
            r'\b(time|date|clock|calendar|schedule)\b',  # Time/date
            r'\b(translate|language|spanish|french|german)\b',  # Translation
            r'\b(news|politics|sports|celebrity|gossip)\b',  # General news
            r'\b(recipe|cooking|food|restaurant|menu)\b',  # Food/cooking
            r'\b(music|song|artist|album|playlist)\b'  # Music
        ]
        
        # Define intent priority order (highest to lowest)
        self.intent_priority = [
            ('unclear', self.unclear_patterns),
            ('out_of_scope', self.out_of_scope_patterns),
            ('greeting', self.greeting_patterns),
            ('thanks', self.thanks_patterns),
            ('document_command', self.document_command_patterns),
            ('system_command', self.system_command_patterns),
            ('summary_request', self.summary_patterns),
            ('data_extraction', self.data_extraction_patterns),
            ('command', self.command_patterns),
        ]
    
    def detect_intent(self, query: str) -> str:
        """
        Detect the intent of a user query
        
        Args:
            query: User's query text
            
        Returns:
            Intent classification: 'greeting', 'thanks', 'command', 'document_command', 
            'system_command', 'summary_request', 'data_extraction', 'unclear', 
            'out_of_scope', 'question'
        """
        query_lower = query.lower().strip()
        
        # Check intents in priority order
        for intent_name, patterns in self.intent_priority:
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent_name
        
        # Default to question intent
        return 'question'
    
    def is_simple_intent(self, intent: str) -> bool:
        """
        Check if an intent should get a simple response (no RAG processing)
        
        Args:
            intent: Detected intent
            
        Returns:
            True if intent requires simple response, False otherwise
        """
        return intent in ['greeting', 'thanks', 'command', 'document_command', 
                         'system_command', 'unclear', 'out_of_scope']
    
    def is_specialized_intent(self, intent: str) -> bool:
        """
        Check if an intent requires specialized processing
        
        Args:
            intent: Detected intent
            
        Returns:
            True if intent requires specialized processing, False otherwise
        """
        return intent in ['summary_request', 'data_extraction']
