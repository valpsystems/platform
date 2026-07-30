from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.constants.enums import ApplicationStatus
from typing import Optional


class CareerRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)
    position: str = Field(..., max_length=200)
    experience_years: Optional[int] = Field(None, ge=0, le=60)
    cover_letter: Optional[str] = Field(None, max_length=5000)
    linkedin_url: Optional[str] = Field(None, max_length=500)
    portfolio_url: Optional[str] = Field(None, max_length=500)


class CareerResponse(BaseModel):
    success: bool = True
    message: str = "Application received successfully"
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CareerDBResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    phone: Optional[str] = None
    position: str
    experience_years: Optional[int] = None
    cover_letter: Optional[str] = None
    resume_path: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    status: str = ApplicationStatus.PENDING
    created_at: datetime
    updated_at: Optional[datetime] = None