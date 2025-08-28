"""
Response Validator Module

Handles response validation and hallucination detection.
"""

import re
from typing import Dict, Any, List, Optional

class ResponseValidator:
    """Validates and checks LLM responses for quality and hallucinations"""
    
    def __init__(self):
        # Patterns for detecting potential hallucinations
        self.hallucination_patterns = [
            r'I don\'t have enough information',
            r'I cannot answer',
            r'I don\'t know',
            r'Based on the provided information',
            r'According to the document',
            r'From the text',
            r'The document states',
            r'As mentioned in'
        ]
        
        # Minimum response length (characters)
        self.min_response_length = 10
        
        # Maximum response length (characters)
        self.max_response_length = 10000
    
    def validate_response(self, response: str) -> Dict[str, Any]:
        """
        Validate response quality and completeness
        
        Args:
            response: LLM response to validate
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'hallucination_risk': False
        }
        
        # Check response length
        if len(response) < self.min_response_length:
            validation_result['is_valid'] = False
            validation_result['issues'].append(f'Response too short ({len(response)} chars, min {self.min_response_length})')
        
        if len(response) > self.max_response_length:
            validation_result['warnings'].append(f'Response very long ({len(response)} chars)')
        
        # Check for empty or whitespace-only responses
        if not response or not response.strip():
            validation_result['is_valid'] = False
            validation_result['issues'].append('Empty or whitespace-only response')
        
        # Check for hallucination patterns
        hallucination_risk = self._check_hallucination_patterns(response)
        if hallucination_risk:
            validation_result['hallucination_risk'] = True
            validation_result['warnings'].append('Potential hallucination detected')
        
        # Check for repeated content
        if self._check_repetition(response):
            validation_result['warnings'].append('Repetitive content detected')
        
        return validation_result
    
    def _check_hallucination_patterns(self, response: str) -> bool:
        """
        Check for patterns that might indicate hallucinations
        
        Args:
            response: Response to check
            
        Returns:
            True if hallucination patterns detected
        """
        response_lower = response.lower()
        
        for pattern in self.hallucination_patterns:
            if re.search(pattern, response_lower):
                return True
        
        return False
    
    def _check_repetition(self, response: str) -> bool:
        """
        Check for repetitive content
        
        Args:
            response: Response to check
            
        Returns:
            True if repetitive content detected
        """
        words = response.split()
        if len(words) < 10:
            return False
        
        # Check for repeated phrases (simple approach)
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Check if any word appears too frequently
        total_words = len(words)
        for word, count in word_counts.items():
            if count / total_words > 0.2:  # Word appears in more than 20% of positions
                return True
        
        return False
    
    def check_response_coherence(self, response: str) -> Dict[str, Any]:
        """
        Check response coherence and structure
        
        Args:
            response: Response to check
            
        Returns:
            Dictionary with coherence analysis
        """
        coherence_result = {
            'has_structure': False,
            'has_complete_sentences': False,
            'avg_sentence_length': 0,
            'sentence_count': 0
        }
        
        # Split into sentences (simple approach)
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        coherence_result['sentence_count'] = len(sentences)
        
        if sentences:
            coherence_result['has_structure'] = True
            
            # Check for complete sentences
            complete_sentences = 0
            total_length = 0
            
            for sentence in sentences:
                if len(sentence.split()) >= 3:  # At least 3 words
                    complete_sentences += 1
                    total_length += len(sentence.split())
            
            coherence_result['has_complete_sentences'] = complete_sentences > 0
            coherence_result['avg_sentence_length'] = total_length / len(sentences) if sentences else 0
        
        return coherence_result
    
    def get_validation_summary(self, validation_result: Dict[str, Any]) -> str:
        """
        Get a summary of validation results
        
        Args:
            validation_result: Validation result dictionary
            
        Returns:
            Summary string
        """
        if validation_result['is_valid'] and not validation_result['warnings']:
            return "Response validation passed"
        
        summary_parts = []
        
        if not validation_result['is_valid']:
            summary_parts.append("Validation failed")
            for issue in validation_result['issues']:
                summary_parts.append(f"- {issue}")
        
        if validation_result['warnings']:
            summary_parts.append("Warnings:")
            for warning in validation_result['warnings']:
                summary_parts.append(f"- {warning}")
        
        return "\n".join(summary_parts)
