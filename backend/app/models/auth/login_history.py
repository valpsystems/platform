from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from .user import User


class LoginHistory(Base):
    __tablename__ = "login_history"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    login_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    device_info: Mapped[str | None] = mapped_column(String(500), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_successful: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    failure_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    session_duration_seconds: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    logout_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    auth_method: Mapped[str] = mapped_column(
        String(50), default="password", nullable=False
    )

    user: Mapped[User] = relationship("User", back_populates="login_history")
