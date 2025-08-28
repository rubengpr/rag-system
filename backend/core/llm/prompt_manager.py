"""
Prompt Manager Module

Handles prompt creation, management, and formatting for LLM interactions.
"""

from typing import Dict, Any, List, Optional

class PromptManager:
    """Manages prompt creation and formatting for LLM interactions"""
    
    def __init__(self):
        # Default prompt templates
        self.default_prompt_template = """
        You are a helpful AI assistant that answers questions based on the provided context.
        Please provide accurate, helpful, and well-structured responses.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer based on the context above:
        """
        
        self.summary_prompt_template = """
        Please provide a comprehensive summary of the following document content. 
        Focus on the key points, main themes, and essential information.
        
        Document Content:
        {content}
        
        Please provide a well-structured summary with:
        1. Main topic/theme
        2. Key points (bullet points)
        3. Important details
        4. Overall conclusion or takeaway
        
        Summary:
        """
        
        self.data_extraction_prompt_template = """
        Please extract and organize the key data from the following document content.
        Focus on structured information, facts, figures, and important details.
        
        Document Content:
        {content}
        
        Please extract and organize the following types of information:
        1. Key Facts and Figures
        2. Important Dates and Timelines
        3. Names, Titles, and Roles
        4. Requirements and Specifications
        5. Benefits and Features
        6. Contact Information or References
        
        Organized Data:
        """
        
        self.simple_response_prompts = {
            'greeting': "You are a helpful AI assistant. Respond warmly to the greeting: {query}",
            'thanks': "You are a helpful AI assistant. Respond courteously to the thanks: {query}",
            'command': "You are a helpful AI assistant. Politely redirect this command to a question: {query}",
            'document_command': "You are a helpful AI assistant. Explain how to manage documents: {query}",
            'system_command': "You are a helpful AI assistant. Acknowledge the system command: {query}",
            'unclear': "You are a helpful AI assistant. Ask for clarification: {query}",
            'out_of_scope': "You are a helpful AI assistant. Politely redirect to document-related questions: {query}"
        }
    
    def create_rag_prompt(self, question: str, context: str, max_tokens: int = 1000) -> str:
        """
        Create a RAG (Retrieval-Augmented Generation) prompt
        
        Args:
            question: User's question
            context: Retrieved context
            max_tokens: Maximum tokens for response
            
        Returns:
            Formatted prompt string
        """
        # Prepare context (limit length to avoid token overflow)
        context_preview = context[:3000] if len(context) > 3000 else context
        
        prompt = self.default_prompt_template.format(
            question=question,
            context=context_preview
        )
        
        # Add token limit instruction
        prompt += f"\n\nPlease provide a clear and concise answer within {max_tokens} words."
        
        return prompt
    
    def create_summary_prompt(self, content: str) -> str:
        """
        Create a summary generation prompt
        
        Args:
            content: Content to summarize
            
        Returns:
            Formatted summary prompt
        """
        return self.summary_prompt_template.format(content=content)
    
    def create_data_extraction_prompt(self, content: str) -> str:
        """
        Create a data extraction prompt
        
        Args:
            content: Content to extract data from
            
        Returns:
            Formatted data extraction prompt
        """
        return self.data_extraction_prompt_template.format(content=content)
    
    def create_simple_intent_prompt(self, intent: str, query: str) -> str:
        """
        Create a prompt for simple intent responses
        
        Args:
            intent: Detected intent
            query: Original user query
            
        Returns:
            Formatted prompt for simple response
        """
        if intent in self.simple_response_prompts:
            return self.simple_response_prompts[intent].format(query=query)
        else:
            return f"You are a helpful AI assistant. Respond appropriately to: {query}"
    
    def format_context_chunks(self, chunks: List[str], max_length: int = 3000) -> str:
        """
        Format context chunks into a single string
        
        Args:
            chunks: List of context chunks
            max_length: Maximum length for combined context
            
        Returns:
            Formatted context string
        """
        if not chunks:
            return ""
        
        # Combine chunks with separators
        combined_context = "\n\n---\n\n".join(chunks)
        
        # Truncate if too long
        if len(combined_context) > max_length:
            combined_context = combined_context[:max_length] + "..."
        
        return combined_context
    
    def create_custom_prompt(self, template: str, **kwargs) -> str:
        """
        Create a custom prompt using a template
        
        Args:
            template: Prompt template string
            **kwargs: Variables to format into template
            
        Returns:
            Formatted prompt string
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required template variable: {e}")
    
    def add_system_instructions(self, prompt: str, instructions: str) -> str:
        """
        Add system instructions to a prompt
        
        Args:
            prompt: Base prompt
            instructions: System instructions to add
            
        Returns:
            Prompt with system instructions
        """
        return f"System Instructions: {instructions}\n\n{prompt}"
    
    def truncate_prompt(self, prompt: str, max_length: int = 4000) -> str:
        """
        Truncate prompt to fit within token limits
        
        Args:
            prompt: Original prompt
            max_length: Maximum length in characters
            
        Returns:
            Truncated prompt
        """
        if len(prompt) <= max_length:
            return prompt
        
        # Truncate and add ellipsis
        return prompt[:max_length-3] + "..."
