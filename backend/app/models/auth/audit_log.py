from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.utils.logger import audit_logger

if TYPE_CHECKING:
    from .user import User


class AuditLog(Base):
    __tablename__ = "audit_logs"

    actor_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    request_method: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    request_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status_code: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    duration_ms: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    performed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    actor: Mapped[Optional[User]] = relationship(
        "User", back_populates="audit_logs", foreign_keys=[actor_id]
    )

    def log_to_logger(self) -> None:
        audit_logger.info(
            f"Audit: {self.action} on {self.resource_type}"
            f"{f'/{self.resource_id}' if self.resource_id else ''}"
            f" by {self.actor_id or 'anonymous'}"
        )