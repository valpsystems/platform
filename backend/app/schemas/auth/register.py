from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.config import settings
from typing import Optional


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=100, description="Unique username")
    password: str = Field(..., min_length=settings.PASSWORD_MIN_LENGTH, description="User password")
    confirm_password: str = Field(..., description="Confirm password")
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError("Username must be a valid identifier (letters, digits, underscores)")
        return v.lower()

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if settings.PASSWORD_REQUIRE_UPPERCASE and not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if settings.PASSWORD_REQUIRE_LOWERCASE and not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if settings.PASSWORD_REQUIRE_DIGIT and not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if settings.PASSWORD_REQUIRE_SPECIAL and not any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?`~" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class RegisterResponse(BaseModel):
    message: str
    user: dict
    requires_email_verification: bool = True