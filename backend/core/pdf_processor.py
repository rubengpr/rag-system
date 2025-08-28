"""
PDF Processing Module

This module handles:
- PDF text extraction
- Text chunking
- Document preprocessing
"""

import PyPDF2
from typing import List, Dict, Any
from models import ChunkInfo
import uuid
import re

class PDFProcessor:
    """Handles PDF file processing and text chunking"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text(self, pdf_file) -> str:
        """Extract text content from a PDF file"""
        try:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text_content = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
            
            # Clean up the text
            cleaned_text = self._clean_text(text_content)
            
            if not cleaned_text.strip():
                raise ValueError("No text content found in PDF")
            
            return cleaned_text
            
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        
        # Normalize line breaks
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def chunk_text(self, text: str, document_id: str) -> List[ChunkInfo]:
        """Split text into overlapping chunks"""
        if not text.strip():
            return []
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Calculate end position for this chunk
            end = start + self.chunk_size
            
            # If this isn't the last chunk, try to break at a word boundary
            if end < len(text):
                # Look for the last space within the last 100 characters
                search_start = max(start + self.chunk_size - 100, start)
                last_space = text.rfind(' ', search_start, end)
                
                if last_space > start:
                    end = last_space
            
            # Extract the chunk
            chunk_text = text[start:end].strip()
            
            if chunk_text:  # Only add non-empty chunks
                chunk = ChunkInfo(
                    id=uuid.uuid4(),
                    content=chunk_text,
                    document_id=document_id,
                    chunk_index=len(chunks)
                )
                chunks.append(chunk)
            
            # Move to next chunk with overlap
            start = end - self.chunk_overlap
            if start >= len(text):
                break
        
        return chunks
    
    def process_pdf(self, pdf_file, filename: str) -> Dict[str, Any]:
        """Process a PDF file and return structured data"""
        try:
            # Generate document ID
            document_id = uuid.uuid4()
            
            # Extract text from PDF
            text_content = self.extract_text(pdf_file)
            
            # Create chunks from text
            chunks = self.chunk_text(text_content, document_id)
            
            # Return structured data
            return {
                "document_id": document_id,
                "filename": filename,
                "text_content": text_content,
                "chunks": chunks,
                "chunk_count": len(chunks),
                "total_characters": len(text_content)
            }
            
        except Exception as e:
            raise ValueError(f"Failed to process PDF '{filename}': {str(e)}")
