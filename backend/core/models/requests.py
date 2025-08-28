"""
Request Models

Contains all API request models with minimal validation.
Complex validation logic is handled by separate validator classes.
"""

from pydantic import BaseModel, Field
from typing import Optional

class FileUploadRequest(BaseModel):
    """Model for file upload requests"""
    pass

class QueryRequest(BaseModel):
    """Model for query requests with basic field validation"""
    query: str = Field(
        ...,  # Required field
        min_length=1,
        max_length=2000,
        description="User query text"
    )
    
    # Optional fields for future extensibility
    session_id: Optional[str] = None
    user_id: Optional[str] = None
