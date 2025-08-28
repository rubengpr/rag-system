"""
API Connector Module

Handles HTTP requests to the Mistral AI API with retry logic and error handling.
"""

import requests
import json
import time
from typing import Dict, Any, Optional, List
from config import settings

class APIConnector:
    """Handles HTTP requests to Mistral AI API"""
    
    def __init__(self):
        self.base_url = settings.MISTRAL_BASE_URL
        self.model = settings.MODEL_NAME
        
        # Request configuration
        self.timeout = 15  # Reduced from 30 to 15 seconds
        self.max_retries = 3  # Reduced from 5 to 3
        self.retry_delay = 1  # Reduced from 2 to 1 second
        
        # Headers for API requests
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def get_authorization_header(self) -> str:
        """
        Get the current authorization header with the latest API key
        
        Returns:
            Authorization header string
        """
        return f"Bearer {settings.MISTRAL_API_KEY}"
    
    def make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the Mistral AI API
        
        Args:
            payload: Request payload
            
        Returns:
            API response as dictionary
            
        Raises:
            Exception: If all retry attempts fail
        """
        # Update authorization header with latest API key
        headers = self.headers.copy()
        headers["Authorization"] = self.get_authorization_header()
        
        for attempt in range(self.max_retries):
            try:
                # Log request size for debugging
                payload_str = json.dumps(payload)
                print(f"REQUEST DEBUG:")
                print(f"  Payload size: {len(payload_str)} characters")
                print(f"  Messages count: {len(payload.get('messages', []))}")
                print(f"  Max tokens: {payload.get('max_tokens', 'Unknown')}")
                
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                # Handle different response status codes
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise Exception(f"API request failed with status 401: {response.text}")
                elif response.status_code == 429:
                    # Rate limit exceeded
                    print(f"RATE LIMIT DEBUG:")
                    print(f"  Status: {response.status_code}")
                    print(f"  Headers: {dict(response.headers)}")
                    print(f"  Limit: {response.headers.get('X-RateLimit-Limit', 'Unknown')}")
                    print(f"  Remaining: {response.headers.get('X-RateLimit-Remaining', 'Unknown')}")
                    print(f"  Reset: {response.headers.get('X-RateLimit-Reset', 'Unknown')}")
                    print(f"  Retry-After: {response.headers.get('Retry-After', 'Unknown')}")
                    
                    if attempt < self.max_retries - 1:
                        wait_time = self._calculate_rate_limit_wait(response)
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception(f"Rate limit exceeded after {self.max_retries} attempts")
                else:
                    raise Exception(f"API request failed with status {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    raise Exception(f"Request timeout after {self.max_retries} attempts")
                    
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    raise Exception(f"Request failed: {str(e)}")
        
        # If we get here, all retries failed
        raise Exception(f"All retry attempts failed")
    
    def _calculate_rate_limit_wait(self, response: requests.Response) -> float:
        """
        Calculate wait time for rate limit response
        
        Args:
            response: Rate limit response
            
        Returns:
            Wait time in seconds
        """
        try:
            # Try to get retry-after header
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                return float(retry_after)
            
            # Try to get rate limit reset time
            reset_time = response.headers.get('X-RateLimit-Reset')
            if reset_time:
                import time
                current_time = int(time.time())
                wait_time = int(reset_time) - current_time
                if wait_time > 0:
                    return float(wait_time) + 1.0  # Add 1 second buffer
            
            # Fallback: exponential backoff with extra buffer
            return 60.0  # Increased to 60 seconds for more conservative approach
            
        except (ValueError, TypeError):
            return 60.0
    
    def create_chat_payload(self, 
                          messages: List[Dict[str, str]], 
                          max_tokens: int = 1000,
                          temperature: float = 0.7,
                          top_p: float = 0.9) -> Dict[str, Any]:
        """
        Create a chat completion payload
        
        Args:
            messages: List of message dictionaries
            max_tokens: Maximum tokens for response
            temperature: Response randomness (0.0-2.0)
            top_p: Nucleus sampling parameter
            
        Returns:
            Request payload dictionary
        """
        return {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
    
    def extract_response_text(self, response: Dict[str, Any]) -> str:
        """
        Extract response text from API response
        
        Args:
            response: API response dictionary
            
        Returns:
            Response text string
            
        Raises:
            Exception: If response format is invalid
        """
        try:
            choices = response.get('choices', [])
            if not choices:
                raise Exception("No choices in API response")
            
            # Get the first choice
            choice = choices[0]
            message = choice.get('message', {})
            content = message.get('content', '')
            
            if not content:
                raise Exception("No content in API response")
            
            return content.strip()
            
        except Exception as e:
            raise Exception(f"Failed to extract response text: {str(e)}")
    
    def validate_response(self, response: Dict[str, Any]) -> bool:
        """
        Validate API response structure
        
        Args:
            response: API response dictionary
            
        Returns:
            True if response is valid
        """
        required_fields = ['choices', 'usage']
        
        for field in required_fields:
            if field not in response:
                return False
        
        choices = response.get('choices', [])
        if not choices:
            return False
        
        choice = choices[0]
        if 'message' not in choice:
            return False
        
        if 'content' not in choice['message']:
            return False
        
        return True
    
    def get_usage_stats(self, response: Dict[str, Any]) -> Dict[str, int]:
        """
        Extract usage statistics from response
        
        Args:
            response: API response dictionary
            
        Returns:
            Dictionary with usage statistics
        """
        usage = response.get('usage', {})
        return {
            'prompt_tokens': usage.get('prompt_tokens', 0),
            'completion_tokens': usage.get('completion_tokens', 0),
            'total_tokens': usage.get('total_tokens', 0)
        }
