"""
LLM Client Module

This module handles:
- Mistral AI API integration
- Prompt management
- Response generation and validation
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional
from config import settings
import re

class MistralClient:
    """Client for interacting with Mistral AI API"""
    
    def __init__(self):
        self.api_key = settings.MISTRAL_API_KEY
        self.base_url = settings.MISTRAL_BASE_URL
        self.model = settings.MODEL_NAME
        

        
        # Request configuration
        self.timeout = 30
        self.max_retries = 5  # Increased retries
        self.retry_delay = 2  # Increased initial delay
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 5.0  # 5 seconds between requests
        self.initial_delay = 5.0  # Wait 5 seconds before first request after startup
        
        # Headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
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
        # Prepare the full prompt with context
        full_prompt = self._prepare_prompt(prompt, context)
        
        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        # Make API request with retries
        for attempt in range(self.max_retries):
            try:
                # Rate limiting: Ensure minimum interval between requests
                current_time = time.time()
                time_since_last = current_time - self.last_request_time
                
                # Initial delay: Wait before first request after startup
                if self.last_request_time == 0:
                    time.sleep(self.initial_delay)
                elif time_since_last < self.min_request_interval:
                    wait_time = self.min_request_interval - time_since_last
                    time.sleep(wait_time)
                
                self.last_request_time = time.time()
                

                
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                # Check if request was successful
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"].strip()
                
                elif response.status_code == 429:  # Rate limit
                    wait_time = self.retry_delay * (2 ** attempt) + 1  # Add extra buffer
                    time.sleep(wait_time)
                    continue
                
                else:
                    error_msg = f"API request failed with status {response.status_code}: {response.text}"
                    
                    if attempt == self.max_retries - 1:
                        raise Exception(error_msg)
                        
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to connect to Mistral API: {str(e)}")
                
                # Wait before retry
                time.sleep(self.retry_delay)
        
        raise Exception("All retry attempts failed")
    
    def create_prompt(self, query: str, context_chunks: List[str]) -> str:
        """
        Create a prompt for the LLM based on query type and context
        
        Args:
            query: User's question
            context_chunks: List of relevant text chunks from search
            
        Returns:
            Formatted prompt for the LLM
        """
        if not context_chunks:
            return self._create_no_context_prompt(query)
        
        # Join context chunks with separators
        context_text = "\n\n---\n\n".join(context_chunks)
        
        # Create the main prompt
        prompt = f"""You are a helpful AI assistant that answers questions based on the provided context. 
You must only use information from the given context to answer the question.

If the context doesn't contain enough information to answer the question accurately, 
respond with "I don't have enough information to answer this question based on the provided context."

Context:
{context_text}

Question: {query}

Please provide a clear, concise answer based only on the information in the context. 
If you need to cite specific parts of the context, mention them briefly."""
        
        return prompt
    
    def _create_no_context_prompt(self, query: str) -> str:
        """
        Create a prompt when no context is available
        
        Args:
            query: User's question
            
        Returns:
            Formatted prompt for cases without context
        """
        return f"""You are a helpful AI assistant. The user has asked a question, but no specific 
context or knowledge base information was provided to answer it.

Question: {query}

Please respond appropriately. If this is a general question that doesn't require 
specific knowledge base information, you can provide a helpful general response. 
If the question requires specific information that should come from a knowledge base, 
let the user know that you don't have the necessary context to answer."""
    
    def _prepare_prompt(self, prompt: str, context: str = "") -> str:
        """
        Prepare the final prompt by combining main prompt and context
        
        Args:
            prompt: Main prompt text
            context: Additional context (if any)
            
        Returns:
            Complete prompt ready for API
        """
        if context:
            return f"{prompt}\n\nAdditional Context: {context}"
        return prompt
    
    def validate_response(self, response: str, context_chunks: List[str]) -> Dict[str, Any]:
        """
        Validate if response is supported by context
        
        Args:
            response: LLM generated response
            context_chunks: List of context chunks used
            
        Returns:
            Dictionary with validation results
        """
        if not context_chunks:
            return {
                "is_valid": True,
                "confidence": 0.5,
                "issues": [],
                "reason": "No context provided for validation"
            }
        
        # Combine all context for validation
        full_context = " ".join(context_chunks).lower()
        response_lower = response.lower()
        
        issues = []
        confidence = 1.0
        
        # Check for common hallucination patterns
        hallucination_indicators = [
            "according to the latest research",
            "recent studies show",
            "experts agree",
            "research indicates",
            "studies have shown"
        ]
        
        for indicator in hallucination_indicators:
            if indicator in response_lower:
                issues.append(f"Contains unsourced claim: '{indicator}'")
                confidence -= 0.1
        
        # Check for specific facts that might not be in context
        # Look for numbers, dates, or specific claims
        specific_claims = re.findall(r'\d{4}', response) + re.findall(r'\d+%', response)
        
        for claim in specific_claims:
            if claim not in full_context:
                issues.append(f"Specific claim not found in context: '{claim}'")
                confidence -= 0.05
        
        # Ensure confidence doesn't go below 0
        confidence = max(0.0, confidence)
        
        return {
            "is_valid": confidence > 0.7,
            "confidence": confidence,
            "issues": issues,
            "reason": f"Validation complete with {len(issues)} issues found"
        }
    
    def create_structured_prompt(self, query: str, context_chunks: List[str], 
                               output_type: str = "general") -> str:
        """
        Create structured prompts for different types of outputs
        
        Args:
            query: User's question
            context_chunks: List of relevant text chunks
            output_type: Type of output desired ("general", "list", "table")
            
        Returns:
            Structured prompt for specific output type
        """
        if not context_chunks:
            return self._create_no_context_prompt(query)
        
        context_text = "\n\n---\n\n".join(context_chunks)
        
        if output_type == "list":
            return f"""Based on the provided context, answer the question by creating a structured list.

Context:
{context_text}

Question: {query}

Please provide your answer as a clear, organized list. Use bullet points or numbered items 
as appropriate. Only include information that is supported by the context."""
        
        elif output_type == "table":
            return f"""Based on the provided context, answer the question by creating a structured table format.

Context:
{context_text}

Question: {query}

Please provide your answer in a table format. If the context contains tabular information, 
present it clearly. If not, organize the information in a logical table structure."""
        
        else:  # general
            return self.create_prompt(query, context_chunks)
