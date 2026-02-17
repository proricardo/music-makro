"""
Music-Makro API - Data Models
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class AnalysisRequest(BaseModel):
    file_name: str = Field(..., description="Nome do arquivo MP3")
    
class AnalysisResponse(BaseModel):
    success: bool
    file_name: str
    analysis_id: str
    timestamp: datetime
    technical_data: Dict[str, Any]
    description: str
    processing_time_seconds: float

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    timestamp: datetime