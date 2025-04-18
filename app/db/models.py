# app/db/models.py
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Download History Model for the database
class DownloadHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    status: str
    downloaded_at: datetime
    filename: str

# Pydantic schema for responses (optional in API)
class DownloadHistoryResponse(BaseModel):
    url: str
    status: str
    downloaded_at: datetime
    filename: str

    class Config:
        orm_mode = True

# Request model to be used in FastAPI for download requests
class DownloadRequest(BaseModel):
    url: str
    format: str = "mp4"
    quality: str = "720p"

# Task Status Response for checking task status
class TaskStatusResponse(BaseModel):
    status: str
    result: Optional[dict]
