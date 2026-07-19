from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.newsletter import NewsletterRepository
from app.schemas.newsletter import NewsletterRequest
from app.services import NewsletterService
from app.utils.response import APIResponse


class NewsletterController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = NewsletterService(NewsletterRepository(session))

    async def subscribe(self, request: NewsletterRequest) -> APIResponse:
        data = await self.service.subscribe(request)
        return APIResponse.created(data=data, message="Subscription successful")
