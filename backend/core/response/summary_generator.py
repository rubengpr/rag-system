"""
Summary Response Generator

Handles generation of summary responses for document content.
"""

import time
from typing import List
from models import QueryRequest, QueryResponse, ChunkInfo
from .base_generator import BaseResponseGenerator

class SummaryGenerator(BaseResponseGenerator):
    """Handles summary request processing"""
    
    def __init__(self, llm_client, search_engine):
        super().__init__(llm_client, search_engine)
        self.summary_chunk_limit = 10
    
    def generate_response(self, request: QueryRequest) -> QueryResponse:
        """
        Generate summary response for the given request
        
        Args:
            request: Query request object
            
        Returns:
            QueryResponse with summary and relevant chunks
        """
        start_time = time.time()
        
        try:
            # Check prerequisites
            if not self.check_documents_available():
                return self.create_error_response(
                    "No documents have been uploaded yet. Please upload some PDF documents first so I can provide a summary.",
                    intent='summary_request'
                )
            
            if not self.check_search_engine_initialized():
                return self.create_error_response(
                    "Search engine not properly initialized. Please try uploading the document again.",
                    intent='summary_request'
                )
            
            # Get chunks for summary
            chunks = self.get_available_chunks(self.summary_chunk_limit)
            
            # Generate summary
            summary_response = self._generate_summary_content(chunks)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            return QueryResponse(
                answer=summary_response,
                chunks=chunks,
                processing_time=processing_time,
                confidence_score=0.9,  # High confidence for summary
                intent='summary_request'
            )
            
        except Exception as e:
            # Fallback to simple response if summary generation fails
            # Check if it's a rate limit error
            if "rate limit" in str(e).lower():
                return self.create_error_response(
                    "I'm currently experiencing high demand. Please wait a moment and try again, or ask a more specific question about your documents.",
                    intent='summary_request'
                )
            else:
                return self.create_error_response(
                    "I encountered an error while generating the summary. Please try again or ask a more specific question about the document content.",
                    intent='summary_request'
                )
    
    def _generate_summary_content(self, chunks: List[ChunkInfo]) -> str:
        """
        Generate summary content from chunks
        
        Args:
            chunks: List of document chunks
            
        Returns:
            Generated summary text
        """
        try:
            # Prepare context for summary
            context = self.format_context_from_chunks(chunks)
            
            # Create specialized summary prompt
            summary_prompt = f"""
            Please provide a comprehensive summary of the following document content. 
            Focus on the key points, main themes, and essential information.
            
            Document Content:
            {context}
            
            Please provide a well-structured summary with:
            1. Main topic/theme
            2. Key points (bullet points)
            3. Important details
            4. Overall conclusion or takeaway
            
            Summary:
            """
            
            # Generate summary using LLM
            result = self.llm_client.generate_response(summary_prompt)
            return result
            
        except Exception as e:
            raise
    
    def process_summary_request(self, request: QueryRequest) -> QueryResponse:
        """
        Process summary requests with specialized handling
        
        Args:
            request: Query request object
            
        Returns:
            QueryResponse with summary and relevant chunks
        """
        return self.generate_response(request)
