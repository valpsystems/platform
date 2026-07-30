from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import Permission
from app.repositories.base import BaseRepository
from typing import Optional


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Permission, session)

    async def get_by_codename(self, codename: str) -> Optional[Permission]:
        result = await self.session.execute(
            select(Permission).where(
                Permission.codename == codename,
                Permission.is_deleted.is_(False),
            )
        )
        return result.scalar_one_or_none()

    async def codename_exists(self, codename: str) -> bool:
        result = await self.session.execute(
            select(func.count()).select_from(Permission).where(
                Permission.codename == codename,
                Permission.is_deleted.is_(False),
            )
        )
        return (result.scalar() or 0) > 0