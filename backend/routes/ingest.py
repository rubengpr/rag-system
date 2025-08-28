"""
Ingest Routes

Handles file upload and processing endpoints
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List
import logging

from models import UploadResponse, DocumentInfo
from config import settings
from core.pdf_processor import PDFProcessor
from storage import storage

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ingest", tags=["ingest"])

# Create rate limiter for ingest routes
limiter = Limiter(key_func=get_remote_address)

def _validate_file(file: UploadFile) -> None:
    """
    Validate uploaded file
    
    Args:
        file: Uploaded file to validate
        
    Raises:
        HTTPException: If file validation fails
    """
    if not file.content_type == "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are allowed"
        )
    
    if file.size > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(
            status_code=400, 
            detail="File size must be less than 10MB"
        )

def _process_pdf_file(file: UploadFile) -> dict:
    """
    Process a single PDF file
    
    Args:
        file: PDF file to process
        
    Returns:
        Processing result with document info and chunks
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        # Initialize PDF processor
        pdf_processor = PDFProcessor(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        # Process the PDF
        result = pdf_processor.process_pdf(file.file, file.filename)
        
        # Store in storage
        storage.add_document(
            result["document_id"],
            {
                "filename": result["filename"],
                "chunk_count": result["chunk_count"],
                "total_characters": result["total_characters"]
            }
        )
        storage.add_chunks(result["document_id"], result["chunks"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file {file.filename}: {str(e)}"
        )

def _initialize_search_engine() -> None:
    """Initialize the search engine with all chunks"""
    try:
        from routes.query import get_rag_pipeline
        pipeline = get_rag_pipeline()
        
        # Convert chunks to ChunkInfo objects if needed
        from models import ChunkInfo
        chunk_infos = []
        for chunk in storage.get_all_chunks():
            if isinstance(chunk, dict):
                chunk_info = ChunkInfo(
                    id=chunk["id"],
                    content=chunk["content"],
                    document_id=chunk["document_id"],
                    chunk_index=chunk["chunk_index"]
                )
                chunk_infos.append(chunk_info)
            else:
                chunk_infos.append(chunk)
        
        # Build search engine with chunks
        pipeline.search_engine.build_tf_idf_vectors(chunk_infos)
        logger.info(f"Search engine initialized with {len(chunk_infos)} chunks")
        
    except Exception as e:
        logger.error(f"Failed to initialize search engine: {str(e)}")
        raise

@router.post("/", response_model=UploadResponse)
@limiter.limit(settings.RATE_LIMIT_UPLOAD)
async def ingest_files(
    request: Request, 
    files: List[UploadFile] = File(...), 
    clear_previous: bool = False
):
    """
    Upload and process PDF files for the knowledge base
    
    Args:
        request: FastAPI request object
        files: List of PDF files to upload
        clear_previous: Whether to clear existing documents
        
    Returns:
        UploadResponse with processed document information
        
    Raises:
        HTTPException: If upload or processing fails
    """
    
    # Clear previous documents if requested
    if clear_previous:
        storage.clear_all()
    
    try:
        # Validate all files
        for file in files:
            _validate_file(file)
        
        # Process each PDF file
        processed_documents = []
        for file in files:
            try:
                result = _process_pdf_file(file)
                
                # Create document info for response
                doc_info = DocumentInfo(
                    id=result["document_id"],
                    filename=result["filename"]
                )
                processed_documents.append(doc_info)
                
            except HTTPException:
                # Re-raise HTTP exceptions
                raise
            except Exception as e:
                # Log error but continue processing other files
                logger.error(f"Error processing file {file.filename}: {str(e)}")
                continue
        
        if not processed_documents:
            raise HTTPException(
                status_code=400, 
                detail="No PDF files were successfully processed"
            )
        
        # Initialize search engine with new chunks
        logger.info(f"Total chunks to initialize: {storage.get_chunk_count()}")
        _initialize_search_engine()
        
        return UploadResponse(documents=processed_documents)
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        # Don't expose internal error details
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error"
        )
