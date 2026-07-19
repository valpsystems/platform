from __future__ import annotations

from sqlalchemy import Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.constants.enums import ApplicationStatus
from app.database.base import Base


class CareerApplication(Base):
    __tablename__ = "career_applications"

    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    position: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    experience_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cover_letter: Mapped[str | None] = mapped_column(Text, nullable=True)
    resume_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    portfolio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        default=ApplicationStatus.PENDING,
        nullable=False,
        index=True,
    )

    __table_args__ = (
        Index("idx_applications_position_status", "position", "status"),
        Index("idx_applications_created_status", "created_at", "status"),
    )
