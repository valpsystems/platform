from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class FeedbackRequest(BaseModel):
    name: str | None = Field(None, max_length=200)
    email: EmailStr | None = None
    rating: int = Field(..., ge=1, le=5)
    category: str | None = Field(None, max_length=100)
    message: str = Field(..., min_length=10, max_length=5000)


class FeedbackResponse(BaseModel):
    success: bool = True
    message: str = "Feedback received successfully"
    data: dict | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FeedbackDBResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str | None = None
    email: str | None = None
    category: str | None = None
    rating: int
    message: str
    created_at: datetime
    updated_at: datetime | None = None
