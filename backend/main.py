from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from typing import List

from models import QueryRequest, QueryResponse, UploadResponse
from config import settings

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
async def ingest_files(files: List[UploadFile] = File(...)):
    """Upload and process PDF files for the knowledge base."""
    try:
        start_time = time.time()
        # TODO: Implement file processing logic
        processing_time = time.time() - start_time
        
        return UploadResponse(
            documents=[]
        )
        
    except Exception as e:
        # Don't expose internal error details to clients
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
