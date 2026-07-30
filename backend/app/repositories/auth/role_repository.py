from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.auth import Role
from app.repositories.base import BaseRepository
from typing import Optional


class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Role, session)

    async def get_by_name(self, name: str) -> Optional[Role]:
        result = await self.session.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.name == name, Role.is_deleted.is_(False))
        )
        return result.unique().scalar_one_or_none()

    async def get_with_permissions(self, role_id: str) -> Optional[Role]:
        result = await self.session.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.id == role_id, Role.is_deleted.is_(False))
        )
        return result.unique().scalar_one_or_none()

    async def name_exists(self, name: str) -> bool:
        result = await self.session.execute(
            select(func.count()).select_from(Role).where(
                Role.name == name,
                Role.is_deleted.is_(False),
            )
        )
        return (result.scalar() or 0) > 0

    async def get_all_with_permissions(self) -> Sequence[Role]:
        result = await self.session.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.is_deleted.is_(False))
        )
        return result.unique().scalars().all()