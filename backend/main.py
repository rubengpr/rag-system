from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
import logging
from typing import List

from models import QueryRequest, QueryResponse, UploadResponse
from config import settings
from core.pdf_processor import PDFProcessor

# Import our query routes
from routes.query import router as query_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for documents and chunks
documents_storage = {}  # document_id -> document_info
chunks_storage = {}     # document_id -> list of chunks
all_chunks = []         # List of all chunks for search engine

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="RAG System API",
    description="A simple RAG pipeline for PDF document processing",
    version="1.0.0"
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only allow needed methods
    allow_headers=["Content-Type", "Authorization"],  # Only allow needed headers
)

# Include query routes
app.include_router(query_router)

# Function to initialize search engine with chunks
def initialize_search_engine():
    """Initialize the search engine with all chunks"""
    global all_chunks
    try:
        from routes.query import get_rag_pipeline
        pipeline = get_rag_pipeline()
        
        # Convert chunks to ChunkInfo objects if needed
        from models import ChunkInfo
        chunk_infos = []
        for chunk in all_chunks:
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

@app.get("/health")
@limiter.limit(settings.RATE_LIMIT_HEALTH)
async def health_check(request: Request):
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/ingest", response_model=UploadResponse)
@limiter.limit(settings.RATE_LIMIT_UPLOAD)
async def ingest_files(request: Request, files: List[UploadFile] = File(...), clear_previous: bool = False):
    """Upload and process PDF files for the knowledge base."""
    
    # Clear previous documents if requested
    if clear_previous:
        documents_storage.clear()
        chunks_storage.clear()
        all_chunks.clear()
    
    try:
        # Security: Validate file types and sizes
        for file in files:
            if not file.content_type == "application/pdf":
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                raise HTTPException(status_code=400, detail="File size must be less than 10MB")
        
        # Initialize PDF processor
        pdf_processor = PDFProcessor(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        # Process each PDF file
        processed_documents = []
        for file in files:
            try:
                # Process the PDF
                result = pdf_processor.process_pdf(file.file, file.filename)
                
                # Store document and chunks in memory
                documents_storage[result["document_id"]] = {
                    "filename": result["filename"],
                    "chunk_count": result["chunk_count"],
                    "total_characters": result["total_characters"]
                }
                chunks_storage[result["document_id"]] = result["chunks"]
                
                # Add chunks to global list for search engine
                all_chunks.extend(result["chunks"])
                
                # Create document info for response
                from models import DocumentInfo
                doc_info = DocumentInfo(
                    id=result["document_id"],
                    filename=result["filename"]
                )
                processed_documents.append(doc_info)
                
            except Exception as e:
                # Log error but continue processing other files
                logger.error(f"Error processing file {file.filename}: {str(e)}")
                continue
        
        if not processed_documents:
            raise HTTPException(status_code=400, detail="No PDF files were successfully processed")
        
        # Initialize search engine with new chunks
        logger.info(f"Total chunks to initialize: {len(all_chunks)}")
        initialize_search_engine()
        
        return UploadResponse(documents=processed_documents)
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        # Don't expose internal error details
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
