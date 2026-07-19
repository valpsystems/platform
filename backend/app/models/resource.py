from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.constants.enums import ContentStatus
from app.database.base import Base


class Resource(Base):
    __tablename__ = "resources"

    title: Mapped[str] = mapped_column(String(300), nullable=False)
    slug: Mapped[str] = mapped_column(String(300), nullable=False)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    author: Mapped[str | None] = mapped_column(String(200), nullable=True)
    published_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tags: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        default=ContentStatus.DRAFT,
        nullable=False,
        index=True,
    )

    __table_args__ = (
        UniqueConstraint("title", name="uq_resources_title"),
        UniqueConstraint("slug", name="uq_resources_slug"),
        Index("idx_resources_category_status", "category", "status"),
        Index("idx_resources_published", "published_date"),
        Index("idx_resources_status_created", "status", "created_at"),
    )
