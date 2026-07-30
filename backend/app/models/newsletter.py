from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.constants.enums import SubscriptionStatus
from app.database.base import Base


class Newsletter(Base):
    __tablename__ = "newsletters"

    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        nullable=False,
        index=True)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        default=SubscriptionStatus.ACTIVE,
        nullable=False)
    subscribed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
    unsubscribed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True)

    __table_args__ = (
        Index("idx_newsletters_status", "status"),
        Index("idx_newsletters_subscribed", "is_subscribed", "subscribed_at"))
