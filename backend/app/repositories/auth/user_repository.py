from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.auth import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.email == email, User.is_deleted.is_(False))
        )
        return result.unique().scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.username == username, User.is_deleted.is_(False))
        )
        return result.unique().scalar_one_or_none()

    async def get_with_roles(self, user_id: str) -> User | None:
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.id == user_id, User.is_deleted.is_(False))
        )
        return result.unique().scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        result = await self.session.execute(
            select(func.count()).select_from(User).where(
                User.email == email,
                User.is_deleted.is_(False),
            )
        )
        return (result.scalar() or 0) > 0

    async def username_exists(self, username: str) -> bool:
        result = await self.session.execute(
            select(func.count()).select_from(User).where(
                User.username == username,
                User.is_deleted.is_(False),
            )
        )
        return (result.scalar() or 0) > 0

    async def get_locked_users(self) -> Sequence[User]:
        result = await self.session.execute(
            select(User).where(
                User.is_locked.is_(True),
                User.is_deleted.is_(False),
            )
        )
        return result.scalars().all()

    async def get_users_by_role(self, role_name: str) -> Sequence[User]:
        from app.models.auth import Role

        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles))
            .join(User.roles)
            .where(Role.name == role_name, User.is_deleted.is_(False))
        )
        return result.unique().scalars().all()
