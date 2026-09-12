from __future__ import annotations

from sqlalchemy import Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.constants.enums import FeedbackCategory
from app.database.base import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    category: Mapped[str | None] = mapped_column(
        String(20),
        default=FeedbackCategory.GENERAL,
        nullable=True,
        index=True,
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        Index("idx_feedbacks_category_rating", "category", "rating"),
        Index("idx_feedbacks_created", "created_at"),
    )
