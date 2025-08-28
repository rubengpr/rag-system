"""
Data Extraction Response Generator

Handles generation of data extraction responses for document content.
"""

import time
from typing import List
from models import QueryRequest, QueryResponse, ChunkInfo
from .base_generator import BaseResponseGenerator

class DataExtractionGenerator(BaseResponseGenerator):
    """Handles data extraction request processing"""
    
    def __init__(self, llm_client, search_engine):
        super().__init__(llm_client, search_engine)
        self.extraction_chunk_limit = 15
    
    def generate_response(self, request: QueryRequest) -> QueryResponse:
        """
        Generate data extraction response for the given request
        
        Args:
            request: Query request object
            
        Returns:
            QueryResponse with extracted data in structured format
        """
        start_time = time.time()
        
        try:
            # Check prerequisites
            if not self.check_documents_available():
                return self.create_error_response(
                    "No documents have been uploaded yet. Please upload some PDF documents first so I can extract data.",
                    intent='data_extraction'
                )
            
            if not self.check_search_engine_initialized():
                return self.create_error_response(
                    "Search engine not properly initialized. Please try uploading the document again.",
                    intent='data_extraction'
                )
            
            # Get chunks for data extraction
            chunks = self.get_available_chunks(self.extraction_chunk_limit)
            
            # Generate data extraction
            extraction_response = self._generate_extraction_content(chunks)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            return QueryResponse(
                answer=extraction_response,
                chunks=chunks,
                processing_time=processing_time,
                confidence_score=0.9,  # High confidence for data extraction
                intent='data_extraction'
            )
            
        except Exception as e:
            # Fallback to simple response if data extraction fails
            return self.create_error_response(
                "I encountered an error while extracting data. Please try again or ask a more specific question about the document content.",
                intent='data_extraction'
            )
    
    def _generate_extraction_content(self, chunks: List[ChunkInfo]) -> str:
        """
        Generate data extraction content from chunks
        
        Args:
            chunks: List of document chunks
            
        Returns:
            Generated data extraction text
        """
        # Prepare context for data extraction
        context = self.format_context_from_chunks(chunks)
        
        # Create specialized data extraction prompt
        extraction_prompt = f"""
        Please extract and organize the key data from the following document content.
        Focus on identifying and structuring the most important information.
        
        Document Content:
        {context}
        
        Please provide a well-structured data extraction with:
        1. **Main Categories/Data Types** found in the document
        2. **Key Data Points** organized by category
        3. **Specific Details** with clear formatting
        4. **Structured Lists** or tables where appropriate
        
        Format the response in a clear, organized manner that makes it easy to read and understand.
        Use bullet points, numbered lists, or tables as appropriate for the data type.
        
        Extracted Data:
        """
        
        # Generate data extraction using LLM
        return self.llm_client.generate_response(extraction_prompt)
    
    def process_data_extraction_request(self, request: QueryRequest) -> QueryResponse:
        """
        Process data extraction requests with specialized handling
        
        Args:
            request: Query request object
            
        Returns:
            QueryResponse with extracted data in structured format
        """
        return self.generate_response(request)
