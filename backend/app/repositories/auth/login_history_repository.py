from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import LoginHistory
from app.repositories.base import BaseRepository


class LoginHistoryRepository(BaseRepository[LoginHistory]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(LoginHistory, session)

    async def get_by_user(self, user_id: str, limit: int = 20) -> Sequence[LoginHistory]:
        result = await self.session.execute(
            select(LoginHistory)
            .where(
                LoginHistory.user_id == user_id,
                LoginHistory.is_deleted.is_(False),
            )
            .order_by(LoginHistory.login_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_recent_failures(
        self, user_id: str, minutes: int = 15
    ) -> Sequence[LoginHistory]:
        from datetime import UTC, datetime, timedelta

        cutoff = datetime.now(UTC) - timedelta(minutes=minutes)
        result = await self.session.execute(
            select(LoginHistory)
            .where(
                LoginHistory.user_id == user_id,
                LoginHistory.is_successful.is_(False),
                LoginHistory.login_at >= cutoff,
                LoginHistory.is_deleted.is_(False),
            )
            .order_by(LoginHistory.login_at.desc())
        )
        return result.scalars().all()
