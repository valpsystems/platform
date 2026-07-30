from __future__ import annotations

from datetime import datetime, timezone

from app.constants.enums import SubscriptionStatus
from app.emails import EmailService
from app.repositories.newsletter import NewsletterRepository
from app.schemas.newsletter import NewsletterRequest
from app.utils.logger import app_logger


class NewsletterService:
    def __init__(self, repository: NewsletterRepository) -> None:
        self.repository = repository
        self.email_service = EmailService()

    async def subscribe(self, request: NewsletterRequest) -> dict:
        app_logger.info(
            "Processing newsletter subscription",
            email=request.email,
            name=request.name)

        existing = await self.repository.first(email=request.email)
        if existing:
            if not existing.is_subscribed:
                await self.repository.update(
                    existing.id,
                    is_subscribed=True,
                    status=SubscriptionStatus.ACTIVE,
                    unsubscribed_at=None)
            subscriber = existing
        else:
            subscriber = await self.repository.create(
                email=request.email,
                name=request.name,
                is_subscribed=True,
                status=SubscriptionStatus.ACTIVE,
                subscribed_at=datetime.now(timezone.utc))

        await self.email_service.send_newsletter_confirmation(
            email=request.email,
            name=request.name or "Subscriber")

        return {
            "id": subscriber.id,
            "email": subscriber.email,
            "name": subscriber.name,
            "status": subscriber.status,
        }
