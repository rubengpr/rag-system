"""
Query Routes

Handles knowledge base query endpoints
"""

from fastapi import APIRouter, HTTPException
from models import QueryRequest, QueryResponse
from core.rag_pipeline import RAGPipeline
import time

router = APIRouter(prefix="/query", tags=["query"])

@router.post("/", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """Query the knowledge base with a question"""
    # TODO: Implement query processing logic
    pass
