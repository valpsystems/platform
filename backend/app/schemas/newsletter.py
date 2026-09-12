from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class NewsletterRequest(BaseModel):
    email: EmailStr
    name: str | None = Field(None, max_length=200)


class NewsletterResponse(BaseModel):
    success: bool = True
    message: str = "Subscription successful"
    data: dict | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class NewsletterDBResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    name: str | None = None
    is_subscribed: bool = True
    status: str = "active"
    subscribed_at: datetime
    unsubscribed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None
