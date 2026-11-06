from __future__ import annotations

from typing import Any

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=1, description="User password")
    remember_me: bool = Field(default=False, description="Extend token expiry")


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict[str, Any]


class TokenRefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token value")
