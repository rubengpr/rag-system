"""
Query Routes

Handles knowledge base query endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from models import QueryRequest, QueryResponse
from core.rag_pipeline import RAGPipeline
from slowapi import Limiter
from slowapi.util import get_remote_address
from config import settings
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/query", tags=["query"])

# Create rate limiter for query routes
limiter = Limiter(key_func=get_remote_address)

# Global RAG pipeline instance
rag_pipeline = None

def get_rag_pipeline():
    """Get or create RAG pipeline instance"""
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline



@router.post("/", response_model=QueryResponse)
@limiter.limit(settings.RATE_LIMIT_QUERY)
async def query_knowledge_base(
    request: Request,
    query_request: QueryRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline)
) -> QueryResponse:
    """
    Query the knowledge base with a question
    
    Args:
        request: Query request containing the user's question
        pipeline: RAG pipeline instance
        
    Returns:
        QueryResponse with answer and supporting chunks
        
    Raises:
        HTTPException: If query processing fails
    """
    start_time = time.time()
    
    try:
        # Validate request
        if not query_request.query or not query_request.query.strip():
            raise HTTPException(
                status_code=400, 
                detail="Query cannot be empty"
            )
        
        # Log the incoming query
        logger.info(f"Processing query: {query_request.query[:100]}...")
        
        # Process query through RAG pipeline
        response = pipeline.process_query(query_request)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Log response details
        logger.info(f"Query processed in {processing_time:.2f}s with {len(response.chunks)} chunks")
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


