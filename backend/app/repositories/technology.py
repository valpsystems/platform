from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.technology import Technology
from app.repositories.base import BaseRepository


class TechnologyRepository(BaseRepository[Technology]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Technology, session)
