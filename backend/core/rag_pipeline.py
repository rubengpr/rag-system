"""
RAG Pipeline Module

This module orchestrates the complete RAG pipeline using modular components:
- Intent detection
- Query processing
- Search and retrieval
- Response generation
"""

from typing import List, Dict, Any, Optional, Tuple
from models import QueryRequest, QueryResponse, ChunkInfo
from .search import SearchEngine
from .llm import MistralClient
from .intent_detector import IntentDetector
from .query_processor import QueryProcessor
from .response_generator import ResponseGenerator
import time

class RAGPipeline:
    """Main RAG pipeline orchestrator"""
    
    def __init__(self):
        # Initialize core components
        self.search_engine = SearchEngine()
        self.llm_client = MistralClient()
        
        # Initialize modular components
        self.intent_detector = IntentDetector()
        self.query_processor = QueryProcessor()
        self.response_generator = ResponseGenerator(self.llm_client, self.search_engine)
        
        # Query processing configuration
        self.min_similarity_threshold = 0.1  # Lowered for testing
        self.max_context_chunks = 5
    
    def process_query(self, request: QueryRequest) -> QueryResponse:
        """
        Process a user query through the complete RAG pipeline
        
        Args:
            request: Query request object
            
        Returns:
            QueryResponse with answer and metadata
        """
        start_time = time.time()
        
        try:
            # Step 1: Intent detection and validation
            intent, refusal_reason = self._detect_intent_and_validate(request)
            if refusal_reason:
                return self._create_refusal_response(refusal_reason)
            
            # Step 2: Handle simple and specialized intents
            simple_response = self._handle_simple_intents(intent, request)
            if simple_response:
                return simple_response
            
            # Step 3: Process complex queries
            return self._process_complex_query(request, intent, start_time)
            
        except Exception as e:
            return self._create_error_response(start_time)
    
    def _detect_intent_and_validate(self, request: QueryRequest) -> Tuple[str, Optional[str]]:
        """
        Detect intent and validate query for sensitive content
        
        Args:
            request: Query request object
            
        Returns:
            Tuple of (intent, refusal_reason)
        """
        intent = self.intent_detector.detect_intent(request.query)
        refusal_reason = self.query_processor.check_query_refusal(request.query)
        return intent, refusal_reason
    
    def _create_refusal_response(self, refusal_reason: str) -> QueryResponse:
        """Create a response for refused queries"""
        return QueryResponse(
            answer=f"I cannot answer this query: {refusal_reason}",
            chunks=[]
        )
    
    def _handle_simple_intents(self, intent: str, request: QueryRequest) -> Optional[QueryResponse]:
        """
        Handle simple and specialized intents
        
        Args:
            intent: Detected intent
            request: Query request object
            
        Returns:
            QueryResponse if handled, None if needs complex processing
        """
        # Handle simple intents with short, concise responses
        if self.intent_detector.is_simple_intent(intent):
            return self.response_generator.generate_simple_intent_response(intent, request.query)
        
        # Handle specialized intents with custom processing
        if intent == 'summary_request':
            return self.response_generator.process_summary_request(request)
        
        if intent == 'data_extraction':
            return self.response_generator.process_data_extraction_request(request)
        
        return None  # Needs complex processing
    
    def _process_complex_query(self, request: QueryRequest, intent: str, start_time: float) -> QueryResponse:
        """
        Process complex queries that require search and LLM generation
        
        Args:
            request: Query request object
            intent: Detected intent
            start_time: Start time for processing
            
        Returns:
            QueryResponse with generated answer
        """
        try:
            # Step 1: Transform query
            transformed_query = self.query_processor.transform_query(request.query)
            
            # Step 2: Validate search engine state
            validation_result = self._validate_search_engine_state()
            if not validation_result['is_valid']:
                return self._create_error_response(start_time, validation_result['message'])
            
            # Step 3: Perform search
            search_results = self.search_engine.search(transformed_query, top_k=self.max_context_chunks, threshold=self.min_similarity_threshold)
            if not search_results:
                return self._handle_no_search_results(transformed_query, intent, start_time)
            
            # Step 4: Process search results
            return self._process_search_results(search_results, transformed_query, intent, start_time)
            
        except Exception as e:
            raise
    
    def _validate_search_engine_state(self) -> Dict[str, Any]:
        """
        Validate that search engine is properly initialized
        
        Returns:
            Dictionary with validation result
        """
        if not self.search_engine.chunks:
            return {
                'is_valid': False,
                'message': "No documents have been uploaded yet. Please upload some PDF documents first."
            }
        
        if not self.search_engine.tfidf_search.tf_idf_vectors:
            return {
                'is_valid': False,
                'message': "Search engine not properly initialized. Please try uploading the document again."
            }
        
        return {'is_valid': True}
    

    
    def _handle_no_search_results(self, transformed_query: str, intent: str, start_time: float) -> QueryResponse:
        """
        Handle case when no search results are found
        
        Args:
            transformed_query: Transformed query string
            intent: Detected intent
            start_time: Start time for processing
            
        Returns:
            QueryResponse with fallback or error message
        """
        return QueryResponse(
            answer="I don't have enough information to answer this question based on my knowledge base.",
            chunks=[]
        )
    
    def _process_search_results(self, search_results: List, transformed_query: str, intent: str, start_time: float) -> QueryResponse:
        """
        Process search results and generate final response
        
        Args:
            search_results: List of search results
            transformed_query: Transformed query string
            intent: Detected intent
            start_time: Start time for processing
            
        Returns:
            QueryResponse with generated answer
        """
        try:
            # Check similarity threshold
            if not self._validate_search_scores(search_results):
                return self._handle_low_similarity_fallback(transformed_query, intent, start_time)
            
            # Use search results directly (they're already ranked)
            ranked_results = search_results
            
            # Generate response
            return self._generate_final_response(ranked_results, transformed_query, intent, start_time)
            
        except Exception as e:
            raise
    
    def _validate_search_scores(self, search_results: List) -> bool:
        """
        Validate that search results meet similarity threshold
        
        Args:
            search_results: List of search results
            
        Returns:
            True if results are valid, False otherwise
        """
        if not search_results:
            return False
        
        first_result = search_results[0]
        if first_result.score is None or first_result.score < self.min_similarity_threshold:
            return False
        
        return True
    
    def _handle_low_similarity_fallback(self, transformed_query: str, intent: str, start_time: float) -> QueryResponse:
        """
        Handle fallback when search similarity is too low
        
        Args:
            transformed_query: Transformed query string
            intent: Detected intent
            start_time: Start time for processing
            
        Returns:
            QueryResponse with fallback answer
        """
        if self.search_engine.chunks:
            fallback_chunks = self.search_engine.chunks[:2]  # Use first 2 chunks
            context_chunks = [chunk.content for chunk in fallback_chunks]
            answer = self.llm_client.generate_rag_response(transformed_query, context_chunks)
            
            return QueryResponse(
                answer=answer,
                chunks=fallback_chunks,
                processing_time=time.time() - start_time,
                confidence_score=0.5,  # Lower confidence for fallback,
                intent=intent
            )
        else:
            return QueryResponse(
                answer="I don't have enough information to answer this question based on my knowledge base.",
                chunks=[]
            )
    
    def _generate_final_response(self, ranked_results: List, transformed_query: str, intent: str, start_time: float) -> QueryResponse:
        """
        Generate the final response from ranked search results
        
        Args:
            ranked_results: Ranked search results
            transformed_query: Transformed query string
            intent: Detected intent
            start_time: Start time for processing
            
        Returns:
            QueryResponse with final answer
        """
        try:
            # Prepare context for LLM
            context_chunks = [result.chunk.content for result in ranked_results[:3]]
            
            # Generate response
            answer = self.llm_client.generate_rag_response(transformed_query, context_chunks)
            
            # Validate response
            validation = self.llm_client.validate_response_quality(answer)
            
            # Prepare chunks for response
            response_chunks = [result.chunk for result in ranked_results[:3]]
            
            processing_time = time.time() - start_time
            
            # Prepare metadata
            metadata = {
                "intent": intent,
                "transformed_query": transformed_query,
                "total_search_results": len(ranked_results),
                "validation_issues": validation.get("issues", []),
                "validation_confidence": validation.get("confidence", 0.0)
            }
            
            return QueryResponse(
                answer=answer,
                chunks=response_chunks,
                processing_time=processing_time,
                confidence_score=validation.get("confidence", 0.0),
                intent=intent,
                search_score=ranked_results[0].score if ranked_results else 0.0,
                metadata=metadata
            )
            
        except Exception as e:
            raise
    
    def _create_error_response(self, start_time: float, message: str = None) -> QueryResponse:
        """
        Create an error response
        
        Args:
            start_time: Start time for processing
            message: Optional error message
            
        Returns:
            QueryResponse with error message
        """
        processing_time = time.time() - start_time
        error_message = message or "An error occurred while processing your query. Please try again."
        
        return QueryResponse(
            answer=error_message,
            chunks=[],
            processing_time=processing_time,
            confidence_score=0.0
        )
    

    

