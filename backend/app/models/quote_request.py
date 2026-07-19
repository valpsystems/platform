from __future__ import annotations

from sqlalchemy import Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.constants.enums import QuoteStatus
from app.database.base import Base


class QuoteRequest(Base):
    __tablename__ = "quote_requests"

    company: Mapped[str | None] = mapped_column(String(200), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    service: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    project_description: Mapped[str] = mapped_column(Text, nullable=False)
    budget_range: Mapped[str | None] = mapped_column(String(20), nullable=True)
    timeline: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        default=QuoteStatus.PENDING,
        nullable=False,
        index=True,
    )

    __table_args__ = (
        Index("idx_quotes_service_status", "service", "status"),
        Index("idx_quotes_created_status", "created_at", "status"),
    )
