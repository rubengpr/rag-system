"""
Rate Limiter Module

Handles client-side rate limiting for API requests.
"""

import time
from typing import Optional

class RateLimiter:
    """Client-side rate limiter for API requests"""
    
    def __init__(self, min_request_interval: float = 5.0, initial_delay: float = 5.0):
        """
        Initialize rate limiter
        
        Args:
            min_request_interval: Minimum time between requests in seconds
            initial_delay: Delay before first request after startup
        """
        self.min_request_interval = min_request_interval
        self.initial_delay = initial_delay
        self.last_request_time = 0.0
    
    def wait_if_needed(self) -> None:
        """Wait if necessary to respect rate limits"""
        current_time = time.time()
        
        # Initial delay: Wait before first request after startup
        if self.last_request_time == 0:
            time.sleep(self.initial_delay)
        else:
            # Check if enough time has passed since last request
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.min_request_interval:
                wait_time = self.min_request_interval - time_since_last
                time.sleep(wait_time)
        
        # Update last request time
        self.last_request_time = time.time()
    
    def update_last_request_time(self) -> None:
        """Update the last request timestamp"""
        self.last_request_time = time.time()
    
    def get_time_since_last_request(self) -> float:
        """Get time elapsed since last request"""
        return time.time() - self.last_request_time
    
    def reset(self) -> None:
        """Reset the rate limiter state"""
        self.last_request_time = 0.0
    
    def set_intervals(self, min_request_interval: float, initial_delay: Optional[float] = None) -> None:
        """
        Update rate limiting intervals
        
        Args:
            min_request_interval: Minimum time between requests
            initial_delay: Initial delay (optional)
        """
        self.min_request_interval = min_request_interval
        if initial_delay is not None:
            self.initial_delay = initial_delay
