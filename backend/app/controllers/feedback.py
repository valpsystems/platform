from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.feedback import FeedbackRepository
from app.schemas.feedback import FeedbackRequest
from app.services import FeedbackService
from app.utils.response import APIResponse


class FeedbackController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = FeedbackService(FeedbackRepository(session))

    async def submit(self, request: FeedbackRequest) -> APIResponse:
        data = await self.service.process_feedback(request)
        return APIResponse.created(data=data, message="Feedback received successfully")
