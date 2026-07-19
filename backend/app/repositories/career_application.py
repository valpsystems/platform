from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.career_application import CareerApplication
from app.repositories.base import BaseRepository


class CareerApplicationRepository(BaseRepository[CareerApplication]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(CareerApplication, session)
