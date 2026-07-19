from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.newsletter import Newsletter
from app.repositories.base import BaseRepository


class NewsletterRepository(BaseRepository[Newsletter]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Newsletter, session)
