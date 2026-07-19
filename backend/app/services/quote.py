from __future__ import annotations

from app.constants.enums import QuoteStatus
from app.emails import EmailService
from app.repositories.quote_request import QuoteRequestRepository
from app.schemas.quote import QuoteRequest
from app.utils.logger import app_logger


class QuoteService:
    def __init__(self, repository: QuoteRequestRepository) -> None:
        self.repository = repository
        self.email_service = EmailService()

    async def process_quote(self, request: QuoteRequest) -> dict:
        app_logger.info(
            "Processing quote request",
            name=request.name,
            email=request.email,
            service=request.service,
        )

        quote = await self.repository.create(
            company=request.company,
            name=request.name,
            email=request.email,
            phone=request.phone,
            service=request.service,
            project_description=request.project_description,
            budget_range=request.budget_range,
            timeline=request.timeline,
            status=QuoteStatus.PENDING,
        )

        await self.email_service.send_quote_notification(
            name=request.name,
            email=request.email,
            company=request.company or "N/A",
            phone=request.phone or "N/A",
            service=request.service,
            project_description=request.project_description,
            budget_range=request.budget_range or "N/A",
            timeline=request.timeline or "N/A",
        )

        return {
            "id": quote.id,
            "name": quote.name,
            "email": quote.email,
            "service": quote.service,
            "status": quote.status,
        }
