"""
Query Validators

Contains validation logic separated from models for better maintainability.
Handles security validation, content validation, and input sanitization.
"""

import re
from typing import List, Dict, Any, Optional

class QueryValidator:
    """Validates and sanitizes query inputs for security and content"""
    
    def __init__(self):
        # Suspicious patterns for security validation
        self.suspicious_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',  # JavaScript protocol
            r'data:',  # Data URLs
            r'vbscript:',  # VBScript protocol
            r'<iframe.*?>.*?</iframe>',  # Iframe tags
            r'<object.*?>.*?</object>',  # Object tags
            r'<embed.*?>.*?</embed>',  # Embed tags
            r'<link.*?>.*?</link>',  # Link tags
            r'<meta.*?>.*?</meta>',  # Meta tags
            r'<style.*?>.*?</style>',  # Style tags
            r'<form.*?>.*?</form>',  # Form tags
            r'<input.*?>',  # Input tags
            r'<textarea.*?>.*?</textarea>',  # Textarea tags
            r'<select.*?>.*?</select>',  # Select tags
            r'<button.*?>.*?</button>',  # Button tags
            r'<a.*?href.*?>.*?</a>',  # Anchor tags with href
            r'<img.*?>',  # Image tags
            r'<svg.*?>.*?</svg>',  # SVG tags
            r'<canvas.*?>.*?</canvas>',  # Canvas tags
            r'<video.*?>.*?</video>',  # Video tags
            r'<audio.*?>.*?</audio>',  # Audio tags
            r'<source.*?>',  # Source tags
            r'<track.*?>',  # Track tags
            r'<map.*?>.*?</map>',  # Map tags
            r'<area.*?>',  # Area tags
            r'<base.*?>',  # Base tags
            r'<bdo.*?>.*?</bdo>',  # BDO tags
            r'<bdi.*?>.*?</bdi>',  # BDI tags
            r'<br.*?>',  # Break tags
            r'<hr.*?>',  # Horizontal rule tags
            r'<keygen.*?>',  # Keygen tags
            r'<param.*?>',  # Param tags
            r'<wbr.*?>',  # Word break opportunity tags
        ]
        
        # Allowed edge cases for intent detection
        self.allowed_edge_cases = {
            '???', 'hmm', 'huh', 'um', 'uh', 'err', 'umm'
        }
        
        # Allowed command phrases
        self.allowed_commands = {
            'clear all', 'clear everything', 'start over', 
            'new session', 'reset'
        }
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """
        Validate query input for security and content
        
        Args:
            query: User query text to validate
            
        Returns:
            Dictionary with validation results and sanitized query
        """
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'sanitized_query': query
        }
        
        if not query or not query.strip():
            result['is_valid'] = False
            result['errors'].append('Query cannot be empty')
            return result
        
        # Sanitize query
        sanitized = query.strip()
        
        # Check for suspicious patterns
        security_issues = self._check_security_patterns(sanitized)
        if security_issues:
            result['is_valid'] = False
            result['errors'].extend(security_issues)
            return result
        
        # Check content patterns
        content_issues = self._check_content_patterns(sanitized)
        if content_issues:
            result['is_valid'] = False
            result['errors'].extend(content_issues)
            return result
        
        # Check for warnings
        warnings = self._check_warnings(sanitized)
        result['warnings'].extend(warnings)
        
        result['sanitized_query'] = sanitized
        return result
    
    def _check_security_patterns(self, query: str) -> List[str]:
        """Check for potentially malicious content patterns"""
        issues = []
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                issues.append(f'Query contains potentially malicious content: {pattern}')
        
        return issues
    
    def _check_content_patterns(self, query: str) -> List[str]:
        """Check for problematic content patterns"""
        issues = []
        
        # Allow edge cases and commands
        if query in self.allowed_edge_cases or query.lower() in self.allowed_commands:
            return issues
        
        # Check for excessive special characters
        special_char_ratio = len(re.findall(r'[^\w\s]', query)) / len(query) if query else 0
        if special_char_ratio > 0.5:
            issues.append('Query contains too many special characters')
        
        # Check for excessive whitespace
        if len(re.findall(r'\s{5,}', query)) > 0:
            issues.append('Query contains excessive whitespace')
        
        # Check for excessive line breaks
        if query.count('\n') > 5:
            issues.append('Query contains too many line breaks')
        
        # Check for excessive repeated characters
        for char in set(query):
            if char != ' ' and query.count(char) > len(query) * 0.4:
                issues.append(f'Query contains excessive repetition of character: {char}')
        
        return issues
    
    def _check_warnings(self, query: str) -> List[str]:
        """Check for content that generates warnings but doesn't fail validation"""
        warnings = []
        
        # Check for very short queries
        if len(query) < 3:
            warnings.append('Query is very short')
        
        # Check for all caps
        if query.isupper() and len(query) > 5:
            warnings.append('Query is in all caps')
        
        # Check for excessive punctuation
        if query.count('!') > 3 or query.count('?') > 3:
            warnings.append('Query contains excessive punctuation')
        
        return warnings
    
    def sanitize_query(self, query: str) -> str:
        """
        Sanitize query input (basic cleaning)
        
        Args:
            query: Raw query input
            
        Returns:
            Sanitized query string
        """
        if not query:
            return ""
        
        # Remove leading/trailing whitespace
        sanitized = query.strip()
        
        # Normalize whitespace (replace multiple spaces with single)
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')
        
        return sanitized
