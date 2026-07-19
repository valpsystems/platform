from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.constants.enums import ApplicationStatus


class CareerRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str | None = Field(None, max_length=50)
    position: str = Field(..., max_length=200)
    experience_years: int | None = Field(None, ge=0, le=60)
    cover_letter: str | None = Field(None, max_length=5000)
    linkedin_url: str | None = Field(None, max_length=500)
    portfolio_url: str | None = Field(None, max_length=500)


class CareerResponse(BaseModel):
    success: bool = True
    message: str = "Application received successfully"
    data: dict | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CareerDBResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    phone: str | None = None
    position: str
    experience_years: int | None = None
    cover_letter: str | None = None
    resume_path: str | None = None
    linkedin_url: str | None = None
    portfolio_url: str | None = None
    status: str = ApplicationStatus.PENDING
    created_at: datetime
    updated_at: datetime | None = None
