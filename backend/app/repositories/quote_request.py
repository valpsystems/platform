from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quote_request import QuoteRequest
from app.repositories.base import BaseRepository


class QuoteRequestRepository(BaseRepository[QuoteRequest]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(QuoteRequest, session)
