from __future__ import annotations

from datetime import datetime, timezone
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import AuditLog
from app.repositories.base import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(AuditLog, session)

    async def get_by_actor(self, actor_id: str, limit: int = 50) -> Sequence[AuditLog]:
        result = await self.session.execute(
            select(AuditLog)
            .where(
                AuditLog.actor_id == actor_id,
                AuditLog.is_deleted.is_(False))
            .order_by(AuditLog.performed_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_resource(
        self, resource_type: str, resource_id: str, limit: int = 50
    ) -> Sequence[AuditLog]:
        result = await self.session.execute(
            select(AuditLog)
            .where(
                AuditLog.resource_type == resource_type,
                AuditLog.resource_id == resource_id,
                AuditLog.is_deleted.is_(False))
            .order_by(AuditLog.performed_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_action(self, action: str, limit: int = 50) -> Sequence[AuditLog]:
        result = await self.session.execute(
            select(AuditLog)
            .where(
                AuditLog.action == action,
                AuditLog.is_deleted.is_(False))
            .order_by(AuditLog.performed_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def cleanup_old(self, days: int = 90) -> int:
        cutoff = datetime.now(timezone.utc).replace(tzinfo=None)
        cutoff = cutoff.replace(hour=0, minute=0, second=0, microsecond=0)
        from datetime import timedelta, timezone
        cutoff = cutoff - timedelta(days=days)

        result = await self.session.execute(
            select(func.count()).select_from(AuditLog).where(
                AuditLog.performed_at < cutoff
            )
        )
        count = result.scalar() or 0

        await self.session.execute(
            select(AuditLog).where(AuditLog.performed_at < cutoff)
        )
        return count
