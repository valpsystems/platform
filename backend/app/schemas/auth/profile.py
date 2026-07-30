from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    department: Optional[str]
    job_title: Optional[str]
    is_email_verified: bool
    is_superuser: bool
    is_active: bool
    is_locked: bool
    last_login_at: Optional[str]
    password_changed_at: Optional[str]
    require_password_change: bool
    two_factor_enabled: bool
    roles: list[dict] = Field(default_factory=list)
    created_at: Optional[str]
    updated_at: Optional[str]


class ProfileResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    department: Optional[str]
    job_title: Optional[str]
    is_email_verified: bool
    is_superuser: bool
    is_active: bool
    two_factor_enabled: bool
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    created_at: Optional[str]
    updated_at: Optional[str]


class UpdateProfileRequest(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    bio: Optional[str] = Field(default=None)
    department: Optional[str] = Field(default=None, max_length=100)
    job_title: Optional[str] = Field(default=None, max_length=100)
    avatar_url: Optional[str] = Field(default=None, max_length=500)