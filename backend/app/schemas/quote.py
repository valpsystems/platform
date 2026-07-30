from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.constants.enums import QuoteStatus
from typing import Optional


class QuoteRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    company: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=50)
    service: str = Field(..., max_length=200)
    project_description: str = Field(..., min_length=20, max_length=10000)
    budget_range: Optional[str] = Field(None, max_length=200)
    timeline: Optional[str] = Field(None, max_length=200)


class QuoteResponse(BaseModel):
    success: bool = True
    message: str = "Quote request received successfully"
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class QuoteDBResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company: Optional[str] = None
    name: str
    email: str
    phone: Optional[str] = None
    service: str
    project_description: str
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    status: str = QuoteStatus.PENDING
    created_at: datetime
    updated_at: Optional[datetime] = None