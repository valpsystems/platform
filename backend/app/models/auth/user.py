from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from .audit_log import AuditLog
    from .login_history import LoginHistory
    from .refresh_token import RefreshToken
    from .role import Role


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    job_title: Mapped[str | None] = mapped_column(String(100), nullable=True)

    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    login_attempts: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_login_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)

    password_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    require_password_change: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    two_factor_enabled: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    two_factor_secret: Mapped[str | None] = mapped_column(String(255), nullable=True)

    roles: Mapped[list[Role]] = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
        lazy="selectin")

    refresh_tokens: Mapped[list[RefreshToken]] = relationship(
        "RefreshToken", back_populates="user", lazy="selectin",
        cascade="all, delete-orphan")

    login_history: Mapped[list[LoginHistory]] = relationship(
        "LoginHistory", back_populates="user", lazy="selectin",
        cascade="all, delete-orphan")

    audit_logs: Mapped[list[AuditLog]] = relationship(
        "AuditLog", back_populates="actor", lazy="selectin",
        foreign_keys="AuditLog.actor_id")

    def dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "department": self.department,
            "job_title": self.job_title,
            "is_email_verified": self.is_email_verified,
            "is_superuser": self.is_superuser,
            "is_active": self.is_active,
            "is_locked": self.is_locked,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "password_changed_at": self.password_changed_at.isoformat() if self.password_changed_at else None,
            "require_password_change": self.require_password_change,
            "two_factor_enabled": self.two_factor_enabled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        return self.username

    def has_role(self, role_name: str) -> bool:
        return any(r.name == role_name for r in self.roles)

    def has_permission(self, permission: str) -> bool:
        if self.is_superuser:
            return True
        return any(
            perm.codename == permission
            for role in self.roles
            for perm in role.permissions
        )

    def has_permissions(self, *permissions: str) -> bool:
        return all(self.has_permission(p) for p in permissions)

    def increment_login_attempts(self) -> None:
        self.login_attempts = (self.login_attempts or 0) + 1

    def reset_login_attempts(self) -> None:
        self.login_attempts = 0
        self.is_locked = False
        self.locked_until = None


