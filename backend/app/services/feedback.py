from __future__ import annotations

from app.constants.enums import FeedbackCategory
from app.emails import EmailService
from app.repositories.feedback import FeedbackRepository
from app.schemas.feedback import FeedbackRequest
from app.utils.logger import app_logger


class FeedbackService:
    def __init__(self, repository: FeedbackRepository) -> None:
        self.repository = repository
        self.email_service = EmailService()

    async def process_feedback(self, request: FeedbackRequest) -> dict:
        app_logger.info(
            "Processing feedback",
            rating=request.rating,
            category=request.category,
            name=request.name,
        )

        feedback_entry = await self.repository.create(
            name=request.name,
            email=request.email,
            category=request.category or FeedbackCategory.GENERAL,
            rating=request.rating,
            message=request.message,
        )

        await self.email_service.send_feedback_notification(
            name=request.name or "Anonymous",
            email=request.email or "N/A",
            rating=request.rating,
            category=request.category or "General",
            message=request.message,
        )

        return {
            "id": feedback_entry.id,
            "rating": feedback_entry.rating,
            "category": feedback_entry.category,
        }
