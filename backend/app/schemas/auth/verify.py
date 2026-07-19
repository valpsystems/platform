from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class VerifyEmailRequest(BaseModel):
    token: str = Field(..., description="Email verification token")


class ResendVerificationRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
