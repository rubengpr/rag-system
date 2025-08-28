"""
Ingest Routes

Handles file upload and processing endpoints
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from models import UploadResponse
import time

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("/", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and process PDF files"""
    # TODO: Implement file upload and processing logic
    pass
