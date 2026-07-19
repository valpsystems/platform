from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.quote_request import QuoteRequestRepository
from app.schemas.quote import QuoteRequest
from app.services import QuoteService
from app.utils.response import APIResponse


class QuoteController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = QuoteService(QuoteRequestRepository(session))

    async def request(self, quote_request: QuoteRequest) -> APIResponse:
        data = await self.service.process_quote(quote_request)
        return APIResponse.created(data=data, message="Quote request received successfully")
