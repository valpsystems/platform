from __future__ import annotations

from sqlalchemy import Boolean, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.constants.enums import ContentStatus
from app.database.base import Base


class Service(Base):
    __tablename__ = "services"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon: Mapped[str | None] = mapped_column(String(100), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        default=ContentStatus.PUBLISHED,
        nullable=False,
        index=True,
    )

    __table_args__ = (
        UniqueConstraint("title", name="uq_services_title"),
        UniqueConstraint("slug", name="uq_services_slug"),
        Index("idx_services_order", "display_order"),
        Index("idx_services_featured_order", "is_featured", "display_order"),
    )
