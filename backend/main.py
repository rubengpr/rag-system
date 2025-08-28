from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from typing import List

from models import QueryRequest, QueryResponse, UploadResponse
from config import settings
from core.pdf_processor import PDFProcessor

# In-memory storage for documents and chunks
documents_storage = {}  # document_id -> document_info
chunks_storage = {}     # document_id -> list of chunks

# Create FastAPI app
app = FastAPI(
    title="RAG System API",
    description="A simple RAG pipeline for PDF document processing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only allow needed methods
    allow_headers=["Content-Type", "Authorization"],  # Only allow needed headers
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}



@app.post("/ingest", response_model=UploadResponse)
async def ingest_files(files: List[UploadFile] = File(...), clear_previous: bool = False):
    """Upload and process PDF files for the knowledge base."""
    
    # Clear previous documents if requested
    if clear_previous:
        documents_storage.clear()
        chunks_storage.clear()
    
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
                
                # Create document info for response
                from models import DocumentInfo
                doc_info = DocumentInfo(
                    id=result["document_id"],
                    filename=result["filename"]
                )
                processed_documents.append(doc_info)
                
            except Exception as e:
                # Log error but continue processing other files
                continue
        
        if not processed_documents:
            raise HTTPException(status_code=400, detail="No PDF files were successfully processed")
        
        return UploadResponse(documents=processed_documents)
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        # Don't expose internal error details
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """Query the knowledge base with a question."""
    try:
        start_time = time.time()
        # TODO: Implement RAG pipeline logic
        processing_time = time.time() - start_time
        
        return QueryResponse(
            answer="This is a placeholder response. RAG pipeline not yet implemented.",
            chunks=[]
        )
    except Exception as e:
        # Don't expose internal error details to clients
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
