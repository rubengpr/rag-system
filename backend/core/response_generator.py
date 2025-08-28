"""
Response Generation Module

This module orchestrates response generation by delegating to specialized generators
based on the type of request or intent.
"""

from models import QueryRequest, QueryResponse
from .llm import MistralClient
from .search import SearchEngine
from .response import (
    SimpleIntentGenerator,
    SummaryGenerator,
    DataExtractionGenerator
)

class ResponseGenerator:
    """Orchestrates response generation by delegating to specialized generators"""
    
    def __init__(self, llm_client: MistralClient, search_engine: SearchEngine):
        self.llm_client = llm_client
        self.search_engine = search_engine
        
        # Initialize specialized generators
        self.simple_intent_generator = SimpleIntentGenerator(llm_client, search_engine)
        self.summary_generator = SummaryGenerator(llm_client, search_engine)
        self.data_extraction_generator = DataExtractionGenerator(llm_client, search_engine)
    
    def generate_simple_intent_response(self, intent: str, original_query: str) -> QueryResponse:
        """
        Generate short, concise responses for simple intents
        
        Args:
            intent: Detected intent (greeting, thanks, command, document_command, system_command, unclear, out_of_scope)
            original_query: Original user query
            
        Returns:
            QueryResponse with appropriate short response
        """
        return self.simple_intent_generator.generate_simple_intent_response(intent, original_query)
    
    def process_summary_request(self, request: QueryRequest) -> QueryResponse:
        """
        Process summary requests with specialized handling
        
        Args:
            request: Query request object
            
        Returns:
            QueryResponse with summary and relevant chunks
        """
        return self.summary_generator.process_summary_request(request)
    
    def process_data_extraction_request(self, request: QueryRequest) -> QueryResponse:
        """
        Process data extraction requests with specialized handling
        
        Args:
            request: Query request object
            
        Returns:
            QueryResponse with extracted data in structured format
        """
        return self.data_extraction_generator.process_data_extraction_request(request)
