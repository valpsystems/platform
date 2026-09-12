from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.constants.enums import QuoteStatus


class QuoteRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    company: str | None = Field(None, max_length=200)
    phone: str | None = Field(None, max_length=50)
    service: str = Field(..., max_length=200)
    project_description: str = Field(..., min_length=20, max_length=10000)
    budget_range: str | None = Field(None, max_length=200)
    timeline: str | None = Field(None, max_length=200)


class QuoteResponse(BaseModel):
    success: bool = True
    message: str = "Quote request received successfully"
    data: dict | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class QuoteDBResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company: str | None = None
    name: str
    email: str
    phone: str | None = None
    service: str
    project_description: str
    budget_range: str | None = None
    timeline: str | None = None
    status: str = QuoteStatus.PENDING
    created_at: datetime
    updated_at: datetime | None = None
