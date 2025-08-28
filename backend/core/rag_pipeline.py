"""
RAG Pipeline Module

This module orchestrates the complete RAG pipeline:
- Query processing
- Search and retrieval
- Response generation
- Post-processing
"""

from typing import List, Dict, Any
from models import QueryRequest, QueryResponse, ChunkInfo
from .search import SearchEngine
from .llm_client import MistralClient
import time
import re

class RAGPipeline:
    """Main RAG pipeline orchestrator"""
    
    def __init__(self):
        self.search_engine = SearchEngine()
        self.llm_client = MistralClient()
        
        # Query processing configuration
        self.min_similarity_threshold = 0.1  # Lowered for testing
        self.max_context_chunks = 5
        
        # Intent detection patterns
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
        
        # PII detection patterns
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-?\d{2}-?\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
        
        # Medical/legal keywords for refusal
        self.sensitive_keywords = {
            'medical': ['diagnosis', 'treatment', 'symptoms', 'medication', 'doctor', 'patient', 'health'],
            'legal': ['legal advice', 'attorney', 'lawyer', 'contract', 'lawsuit', 'court', 'legal counsel']
        }
    
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
            intent = self.detect_intent(request.query)
            
            # Step 2: Check for sensitive content or PII
            refusal_reason = self.check_query_refusal(request.query)
            if refusal_reason:
                return QueryResponse(
                    answer=f"I cannot answer this query: {refusal_reason}",
                    chunks=[]
                )
            
            # Handle non-question intents with short, concise responses
            if intent in ['greeting', 'thanks', 'command', 'document_command', 'system_command', 'unclear', 'out_of_scope']:
                return self._generate_intent_response(intent, request.query)
            
            # Handle summary requests with specialized processing
            if intent == 'summary_request':
                return self._process_summary_request(request)
            
            # Handle data extraction requests with specialized processing
            if intent == 'data_extraction':
                return self._process_data_extraction_request(request)
            
            # Step 3: Query transformation
            transformed_query = self.transform_query(request.query)
            
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
    
    def detect_intent(self, query: str) -> str:
        """
        Detect the intent of a user query
        
        Args:
            query: User's query text
            
        Returns:
            Intent classification: 'greeting', 'thanks', 'command', 'document_command', 'system_command', 'summary_request', 'data_extraction', 'unclear', 'out_of_scope', 'question'
        """
        query_lower = query.lower().strip()
        
        # Check for unclear/confused queries first (highest priority)
        for pattern in self.unclear_patterns:
            if re.search(pattern, query_lower):
                return 'unclear'
        
        # Check for out-of-scope requests
        for pattern in self.out_of_scope_patterns:
            if re.search(pattern, query_lower):
                return 'out_of_scope'
        
        # Check for greetings
        for pattern in self.greeting_patterns:
            if re.search(pattern, query_lower):
                return 'greeting'
        
        # Check for thanks/acknowledgment
        for pattern in self.thanks_patterns:
            if re.search(pattern, query_lower):
                return 'thanks'
        
        # Check for document management commands
        for pattern in self.document_command_patterns:
            if re.search(pattern, query_lower):
                return 'document_command'
        
        # Check for system commands
        for pattern in self.system_command_patterns:
            if re.search(pattern, query_lower):
                return 'system_command'
        
        # Check for summary requests
        for pattern in self.summary_patterns:
            if re.search(pattern, query_lower):
                return 'summary_request'
        
        # Check for data extraction requests
        for pattern in self.data_extraction_patterns:
            if re.search(pattern, query_lower):
                return 'data_extraction'
        
        # Check for general commands
        for pattern in self.command_patterns:
            if re.search(pattern, query_lower):
                return 'command'
        
        # Default to question intent
        return 'question'
    
    def transform_query(self, query: str) -> str:
        """
        Transform query for better retrieval effectiveness
        
        Args:
            query: Original user query
            
        Returns:
            Transformed query optimized for search
        """
        # Remove common filler words that don't help with search
        filler_words = ['what is', 'what are', 'can you', 'please', 'tell me']
        transformed = query.lower()
        
        for filler in filler_words:
            transformed = transformed.replace(filler, ' ').strip()
        
        # Expand common acronyms
        acronym_expansions = {
            'ai': 'artificial intelligence',
            'ml': 'machine learning',
            'dl': 'deep learning',
            'api': 'application programming interface',
            'ui': 'user interface',
            'ux': 'user experience'
        }
        
        for acronym, expansion in acronym_expansions.items():
            # Replace standalone acronyms (word boundaries)
            transformed = re.sub(r'\b' + acronym + r'\b', expansion, transformed)
        
        # Remove excessive whitespace
        transformed = ' '.join(transformed.split())
        
        # If transformation made query too short, use original
        if len(transformed) < 3:
            transformed = query
        
        return transformed
    
    def check_query_refusal(self, query: str) -> str:
        """
        Check if query should be refused due to sensitive content or PII
        
        Args:
            query: User query to check
            
        Returns:
            Refusal reason if query should be refused, empty string otherwise
        """
        query_lower = query.lower()
        
        # Check for PII patterns
        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, query):
                return f"Query contains potential {pii_type.upper()} information"
        
        # Check for medical/legal content
        for category, keywords in self.sensitive_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return f"Query appears to request {category} advice, which I cannot provide"
        
        # Check for other sensitive patterns
        sensitive_patterns = [
            r'\b(personal|private|confidential)\b',
            r'\b(password|secret|security)\b'
        ]
        
        for pattern in sensitive_patterns:
            if re.search(pattern, query_lower):
                return "Query contains potentially sensitive information"
        
        return ""  # No refusal reason
    
    def _generate_intent_response(self, intent: str, original_query: str) -> QueryResponse:
        """
        Generate short, concise responses for non-question intents
        
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
            chunks=[],  # No chunks for non-question intents
            processing_time=0.0,  # No processing time for simple responses
            confidence_score=1.0,  # High confidence for simple responses
            intent=intent
        )
    
    def _process_summary_request(self, request: QueryRequest) -> QueryResponse:
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
    
    def _process_data_extraction_request(self, request: QueryRequest) -> QueryResponse:
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
