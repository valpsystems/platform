from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resource import Resource
from app.repositories.base import BaseRepository


class ResourceRepository(BaseRepository[Resource]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Resource, session)
