from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(__import__("uuid").uuid4()))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True)

    created_by: Mapped[Optional[str]] = mapped_column(
        String(36),
        nullable=True)

    updated_by: Mapped[Optional[str]] = mapped_column(
        String(36),
        nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False)

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False)

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True)

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False)

    def dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def soft_delete(self) -> None:
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        self.is_deleted = False
        self.is_active = True
        self.deleted_at = None