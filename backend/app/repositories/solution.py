from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.solution import Solution
from app.repositories.base import BaseRepository


class SolutionRepository(BaseRepository[Solution]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Solution, session)
