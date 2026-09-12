from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.constants.enums import ContactStatus


class ContactRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    company: str | None = Field(None, max_length=200)
    phone: str | None = Field(None, max_length=50)
    subject: str | None = Field(None, max_length=500)
    message: str = Field(..., min_length=10, max_length=5000)


class ContactResponse(BaseModel):
    success: bool = True
    message: str = "Contact request received successfully"
    data: dict | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ContactDBResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    company: str | None = None
    phone: str | None = None
    subject: str | None = None
    message: str
    status: str = ContactStatus.PENDING
    notes: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    is_active: bool = True
