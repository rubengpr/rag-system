"""
RAG Pipeline Module

This module orchestrates the complete RAG pipeline using modular components:
- Intent detection
- Query processing
- Search and retrieval
- Response generation
"""

from typing import List, Dict, Any
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
            # Step 1: Query intent detection
            intent = self.intent_detector.detect_intent(request.query)
            
            # Step 2: Check for sensitive content or PII
            refusal_reason = self.query_processor.check_query_refusal(request.query)
            if refusal_reason:
                return QueryResponse(
                    answer=f"I cannot answer this query: {refusal_reason}",
                    chunks=[]
                )
            
            # Handle simple intents with short, concise responses
            if self.intent_detector.is_simple_intent(intent):
                return self.response_generator.generate_simple_intent_response(intent, request.query)
            
            # Handle specialized intents with custom processing
            if intent == 'summary_request':
                return self.response_generator.process_summary_request(request)
            
            if intent == 'data_extraction':
                return self.response_generator.process_data_extraction_request(request)
            
            # Step 3: Query transformation
            transformed_query = self.query_processor.transform_query(request.query)
            
            # Step 4: Chunks check
            if not self.search_engine.chunks:
                return QueryResponse(
                    answer="No documents have been uploaded yet. Please upload some PDF documents first.",
                    chunks=[]
                )
            
            # Step 5: TF-IDF vectors check
            if not self.search_engine.tf_idf_vectors:
                return QueryResponse(
                    answer="Search engine not properly initialized. Please try uploading the document again.",
                    chunks=[]
                )
            
            search_results = self.search_engine.hybrid_search(
                transformed_query, 
                self.search_engine.chunks, 
                self.max_context_chunks
            )
            

            
            # Step 5: Check similarity threshold
            if not search_results:
                return QueryResponse(
                    answer="I don't have enough information to answer this question based on my knowledge base.",
                    chunks=[]
                )
            
            # Ensure score is a valid number
            if search_results[0].score is None or search_results[0].score < self.min_similarity_threshold:
                # Fallback: use first few chunks if search fails
                if self.search_engine.chunks:
                    fallback_chunks = self.search_engine.chunks[:2]  # Use first 2 chunks
                    context_chunks = [chunk.content for chunk in fallback_chunks]
                    prompt = self.llm_client.create_prompt(transformed_query, context_chunks)
                    answer = self.llm_client.generate_response(prompt)
                    
                    return QueryResponse(
                        answer=answer,
                        chunks=fallback_chunks,
                        processing_time=time.time() - start_time,
                        confidence_score=0.5,  # Lower confidence for fallback
                        intent=intent
                    )
                else:
                    return QueryResponse(
                        answer="I don't have enough information to answer this question based on my knowledge base.",
                        chunks=[]
                    )
            
            # Step 6: Re-rank results
            ranked_results = self.search_engine.rank_results(search_results)
            
            # Step 7: Prepare context for LLM
            context_chunks = [result.chunk.content for result in ranked_results[:3]]
            
            # Step 8: Generate response
            prompt = self.llm_client.create_prompt(transformed_query, context_chunks)
            answer = self.llm_client.generate_response(prompt)
            
            # Step 9: Validate response
            validation = self.llm_client.validate_response(answer, context_chunks)
            
            # Step 10: Prepare chunks for response
            response_chunks = []
            for result in ranked_results[:3]:
                response_chunks.append(result.chunk)
            
            processing_time = time.time() - start_time
            
            # Prepare metadata
            metadata = {
                "intent": intent,
                "transformed_query": transformed_query,
                "total_search_results": len(search_results),
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
            # Handle any errors gracefully
            processing_time = time.time() - start_time
            return QueryResponse(
                answer="An error occurred while processing your query. Please try again.",
                chunks=[]
            )
    

    

