"""
Simple Intent Response Generator

Handles generation of responses for simple intents like greetings, thanks, commands, etc.
"""

from typing import Dict
from models import QueryRequest, QueryResponse
from .base_generator import BaseResponseGenerator

class SimpleIntentGenerator(BaseResponseGenerator):
    """Handles simple intent responses"""
    
    def __init__(self, llm_client, search_engine):
        super().__init__(llm_client, search_engine)
        self._response_templates = self._initialize_response_templates()
    
    def _initialize_response_templates(self) -> Dict[str, str]:
        """Initialize response templates for different intents"""
        return {
            'greeting': "Hello! I'm here to help you with questions about your documents. Feel free to ask me anything!",
            'thanks': "You're welcome! I'm glad I could help. Let me know if you have any other questions!",
            'command': "I understand you've given me a command. I'm designed to answer questions about your documents. Could you please rephrase that as a question?",
            'document_command': "For document management, use the file upload interface above. I can help you analyze the content once it's uploaded.",
            'system_command': "I'll start fresh. Please upload your documents again and I'll be ready to help.",
            'unclear': "I'm not sure what you're asking. Could you please rephrase your question? For example: 'What is this document about?' or 'Summarize the key points.'",
            'out_of_scope': "I'm designed to help with questions about your uploaded documents. Please ask me about the content in your knowledge base.",
            'default': "I'm here to help! Please ask me a question about your documents."
        }
    
    def generate_response(self, request: QueryRequest) -> QueryResponse:
        """
        Generate response for simple intents
        
        Args:
            request: Query request object
            
        Returns:
            QueryResponse with appropriate simple response
        """
        # Extract intent from request (assuming it's passed in the request or determined elsewhere)
        intent = getattr(request, 'intent', 'default')
        
        # Get response template
        response_text = self._response_templates.get(intent, self._response_templates['default'])
        
        return QueryResponse(
            answer=response_text,
            chunks=[],  # No chunks for simple intents
            processing_time=0.0,  # No processing time for simple responses
            confidence_score=1.0,  # High confidence for simple responses
            intent=intent
        )
    
    def generate_simple_intent_response(self, intent: str, original_query: str) -> QueryResponse:
        """
        Generate short, concise responses for simple intents
        
        Args:
            intent: Detected intent (greeting, thanks, command, document_command, system_command, unclear, out_of_scope)
            original_query: Original user query
            
        Returns:
            QueryResponse with appropriate short response
        """
        # Get response template directly
        response_text = self._response_templates.get(intent, self._response_templates['default'])
        
        return QueryResponse(
            answer=response_text,
            chunks=[],  # No chunks for simple intents
            processing_time=0.0,  # No processing time for simple responses
            confidence_score=1.0,  # High confidence for simple responses
            intent=intent
        )
