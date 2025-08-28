"""
Response Generation Module

This module handles specialized response generation for different intent types.
It includes simple intent responses and specialized processing for summary and data extraction.
"""

import time
from typing import List
from models import QueryRequest, QueryResponse, ChunkInfo
from .llm_client import MistralClient
from .search import SearchEngine

class ResponseGenerator:
    """Handles specialized response generation for different intents"""
    
    def __init__(self, llm_client: MistralClient, search_engine: SearchEngine):
        self.llm_client = llm_client
        self.search_engine = search_engine
    
    def generate_simple_intent_response(self, intent: str, original_query: str) -> QueryResponse:
        """
        Generate short, concise responses for simple intents
        
        Args:
            intent: Detected intent (greeting, thanks, command, document_command, system_command, unclear, out_of_scope)
            original_query: Original user query
            
        Returns:
            QueryResponse with appropriate short response
        """
        if intent == 'greeting':
            response = "Hello! I'm here to help you with questions about your documents. Feel free to ask me anything!"
        elif intent == 'thanks':
            response = "You're welcome! I'm glad I could help. Let me know if you have any other questions!"
        elif intent == 'command':
            response = "I understand you've given me a command. I'm designed to answer questions about your documents. Could you please rephrase that as a question?"
        elif intent == 'document_command':
            response = "For document management, use the file upload interface above. I can help you analyze the content once it's uploaded."
        elif intent == 'system_command':
            response = "I'll start fresh. Please upload your documents again and I'll be ready to help."
        elif intent == 'unclear':
            response = "I'm not sure what you're asking. Could you please rephrase your question? For example: 'What is this document about?' or 'Summarize the key points.'"
        elif intent == 'out_of_scope':
            response = "I'm designed to help with questions about your uploaded documents. Please ask me about the content in your knowledge base."
        else:
            response = "I'm here to help! Please ask me a question about your documents."
        
        return QueryResponse(
            answer=response,
            chunks=[],  # No chunks for simple intents
            processing_time=0.0,  # No processing time for simple responses
            confidence_score=1.0,  # High confidence for simple responses
            intent=intent
        )
    
    def process_summary_request(self, request: QueryRequest) -> QueryResponse:
        """
        Process summary requests with specialized handling
        
        Args:
            request: Query request object
            
        Returns:
            QueryResponse with summary and relevant chunks
        """
        start_time = time.time()
        
        try:
            # Check if we have documents to summarize
            if not self.search_engine.chunks:
                return QueryResponse(
                    answer="No documents have been uploaded yet. Please upload some PDF documents first so I can provide a summary.",
                    chunks=[],
                    intent='summary_request'
                )
            
            # Check if TF-IDF vectors are initialized
            if not self.search_engine.tf_idf_vectors:
                return QueryResponse(
                    answer="Search engine not properly initialized. Please try uploading the document again.",
                    chunks=[],
                    intent='summary_request'
                )
            
            # Get all available chunks for comprehensive summary
            all_chunks = self.search_engine.chunks[:10]  # Limit to first 10 chunks for summary
            
            # Prepare context for summary
            context = "\n\n".join([f"Document {chunk.document_id}: {chunk.content}" for chunk in all_chunks])
            
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
            summary_response = self.llm_client.generate_response(summary_prompt)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            return QueryResponse(
                answer=summary_response,
                chunks=all_chunks,
                processing_time=processing_time,
                confidence_score=0.9,  # High confidence for summary
                intent='summary_request'
            )
            
        except Exception as e:
            # Fallback to simple response if summary generation fails
            return QueryResponse(
                answer="I encountered an error while generating the summary. Please try again or ask a more specific question about the document content.",
                chunks=[],
                intent='summary_request'
            )
    
    def process_data_extraction_request(self, request: QueryRequest) -> QueryResponse:
        """
        Process data extraction requests with specialized handling
        
        Args:
            request: Query request object
            
        Returns:
            QueryResponse with extracted data in structured format
        """
        start_time = time.time()
        
        try:
            # Check if we have documents to extract data from
            if not self.search_engine.chunks:
                return QueryResponse(
                    answer="No documents have been uploaded yet. Please upload some PDF documents first so I can extract data.",
                    chunks=[],
                    intent='data_extraction'
                )
            
            # Check if TF-IDF vectors are initialized
            if not self.search_engine.tf_idf_vectors:
                return QueryResponse(
                    answer="Search engine not properly initialized. Please try uploading the document again.",
                    chunks=[],
                    intent='data_extraction'
                )
            
            # Get all available chunks for comprehensive data extraction
            all_chunks = self.search_engine.chunks[:15]  # Limit to first 15 chunks for data extraction
            
            # Prepare context for data extraction
            context = "\n\n".join([f"Document {chunk.document_id}: {chunk.content}" for chunk in all_chunks])
            
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
            extraction_response = self.llm_client.generate_response(extraction_prompt)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            return QueryResponse(
                answer=extraction_response,
                chunks=all_chunks,
                processing_time=processing_time,
                confidence_score=0.9,  # High confidence for data extraction
                intent='data_extraction'
            )
            
        except Exception as e:
            # Fallback to simple response if data extraction fails
            return QueryResponse(
                answer="I encountered an error while extracting data. Please try again or ask a more specific question about the document content.",
                chunks=[],
                intent='data_extraction'
            )
