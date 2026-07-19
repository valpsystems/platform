from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: str | None
    last_name: str | None
    phone: str | None
    avatar_url: str | None
    bio: str | None
    department: str | None
    job_title: str | None
    is_email_verified: bool
    is_superuser: bool
    is_active: bool
    is_locked: bool
    last_login_at: str | None
    password_changed_at: str | None
    require_password_change: bool
    two_factor_enabled: bool
    roles: list[dict] = Field(default_factory=list)
    created_at: str | None
    updated_at: str | None


class ProfileResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: str | None
    last_name: str | None
    phone: str | None
    avatar_url: str | None
    bio: str | None
    department: str | None
    job_title: str | None
    is_email_verified: bool
    is_superuser: bool
    is_active: bool
    two_factor_enabled: bool
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    created_at: str | None
    updated_at: str | None


class UpdateProfileRequest(BaseModel):
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    bio: str | None = Field(default=None)
    department: str | None = Field(default=None, max_length=100)
    job_title: str | None = Field(default=None, max_length=100)
    avatar_url: str | None = Field(default=None, max_length=500)
