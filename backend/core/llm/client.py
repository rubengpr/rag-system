"""
Main LLM Client Module

Orchestrates all LLM components and provides a unified interface for LLM interactions.
"""

from typing import Dict, Any, List, Optional
from .api_connector import APIConnector
from .prompt_manager import PromptManager
from .rate_limiter import RateLimiter
from .validator import ResponseValidator

class MistralClient:
    """Main LLM client that orchestrates API calls, prompts, rate limiting, and validation"""
    
    def __init__(self):
        # Initialize components
        self.api_connector = APIConnector()
        self.prompt_manager = PromptManager()
        self.rate_limiter = RateLimiter()
        self.validator = ResponseValidator()
    
    def generate_response(self, prompt: str, context: str = "", max_tokens: int = 1000) -> str:
        """
        Generate response using Mistral AI API
        
        Args:
            prompt: The main prompt for the LLM
            context: Additional context to include (optional)
            max_tokens: Maximum tokens for response
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If API call fails after retries
        """
        try:
            # Apply rate limiting
            self.rate_limiter.wait_if_needed()
            
            # Prepare the full prompt with context
            full_prompt = self._prepare_prompt(prompt, context)
            
            # Create chat messages
            messages = [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
            
            # Create request payload
            payload = self.api_connector.create_chat_payload(
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9
            )
            
            # Make API request
            response = self.api_connector.make_request(payload)
            
            # Extract response text
            response_text = self.api_connector.extract_response_text(response)
            
            # Validate response
            validation_result = self.validator.validate_response(response_text)
            if not validation_result['is_valid']:
                # Log validation issues but still return the response
                pass
            
            # Update rate limiter
            self.rate_limiter.update_last_request_time()
            
            return response_text
            
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def generate_rag_response(self, question: str, context_chunks: List[str], max_tokens: int = 1000) -> str:
        """
        Generate RAG response with context
        
        Args:
            question: User's question
            context_chunks: List of context chunks
            max_tokens: Maximum tokens for response
            
        Returns:
            Generated response text
        """
        # Format context chunks
        context = self.prompt_manager.format_context_chunks(context_chunks)
        
        # Create RAG prompt
        prompt = self.prompt_manager.create_rag_prompt(question, context, max_tokens)
        
        # Generate response
        return self.generate_response(prompt, max_tokens=max_tokens)
    
    def generate_summary(self, content: str) -> str:
        """
        Generate summary response
        
        Args:
            content: Content to summarize
            
        Returns:
            Generated summary
        """
        # Create summary prompt
        prompt = self.prompt_manager.create_summary_prompt(content)
        
        # Generate response
        return self.generate_response(prompt, max_tokens=800)
    
    def generate_data_extraction(self, content: str) -> str:
        """
        Generate data extraction response
        
        Args:
            content: Content to extract data from
            
        Returns:
            Generated data extraction
        """
        # Create data extraction prompt
        prompt = self.prompt_manager.create_data_extraction_prompt(content)
        
        # Generate response
        return self.generate_response(prompt, max_tokens=1200)
    
    def generate_simple_intent_response(self, intent: str, query: str) -> str:
        """
        Generate response for simple intents
        
        Args:
            intent: Detected intent
            query: Original user query
            
        Returns:
            Generated response
        """
        # Create simple intent prompt
        prompt = self.prompt_manager.create_simple_intent_prompt(intent, query)
        
        # Generate response
        return self.generate_response(prompt, max_tokens=200)
    
    def _prepare_prompt(self, prompt: str, context: str = "") -> str:
        """
        Prepare the full prompt with context
        
        Args:
            prompt: Main prompt
            context: Additional context
            
        Returns:
            Prepared full prompt
        """
        if context:
            # Truncate context if too long
            context = self.prompt_manager.truncate_prompt(context, 3000)
            full_prompt = f"Context: {context}\n\n{prompt}"
        else:
            full_prompt = prompt
        
        # Final truncation to ensure we don't exceed token limits
        return self.prompt_manager.truncate_prompt(full_prompt, 4000)
    
    def validate_response_quality(self, response: str) -> Dict[str, Any]:
        """
        Validate response quality
        
        Args:
            response: Response to validate
            
        Returns:
            Validation results
        """
        return self.validator.validate_response(response)
    
    def get_response_coherence(self, response: str) -> Dict[str, Any]:
        """
        Get response coherence analysis
        
        Args:
            response: Response to analyze
            
        Returns:
            Coherence analysis results
        """
        return self.validator.check_response_coherence(response)
    
    def set_rate_limiting(self, min_request_interval: float, initial_delay: Optional[float] = None) -> None:
        """
        Update rate limiting settings
        
        Args:
            min_request_interval: Minimum time between requests
            initial_delay: Initial delay (optional)
        """
        self.rate_limiter.set_intervals(min_request_interval, initial_delay)
    
    def reset_rate_limiter(self) -> None:
        """Reset the rate limiter state"""
        self.rate_limiter.reset()
    
    def get_rate_limiter_stats(self) -> Dict[str, float]:
        """
        Get rate limiter statistics
        
        Returns:
            Dictionary with rate limiter stats
        """
        return {
            'min_request_interval': self.rate_limiter.min_request_interval,
            'initial_delay': self.rate_limiter.initial_delay,
            'time_since_last_request': self.rate_limiter.get_time_since_last_request()
        }
