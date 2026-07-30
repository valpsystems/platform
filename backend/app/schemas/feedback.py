from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional


class FeedbackRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    rating: int = Field(..., ge=1, le=5)
    category: Optional[str] = Field(None, max_length=100)
    message: str = Field(..., min_length=10, max_length=5000)


class FeedbackResponse(BaseModel):
    success: bool = True
    message: str = "Feedback received successfully"
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FeedbackDBResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    category: Optional[str] = None
    rating: int
    message: str
    created_at: datetime
    updated_at: Optional[datetime] = None