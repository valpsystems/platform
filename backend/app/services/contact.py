from __future__ import annotations

from app.constants.enums import ContactStatus
from app.emails import EmailService
from app.repositories.contact import ContactRepository
from app.schemas.contact import ContactRequest
from app.utils.logger import app_logger


class ContactService:
    def __init__(self, repository: ContactRepository) -> None:
        self.repository = repository
        self.email_service = EmailService()

    async def process_contact(self, request: ContactRequest) -> dict:
        app_logger.info(
            "Processing contact request",
            name=request.name,
            email=request.email,
            company=request.company,
        )

        contact = await self.repository.create(
            name=request.name,
            email=request.email,
            company=request.company,
            phone=request.phone,
            subject=request.subject,
            message=request.message,
            status=ContactStatus.PENDING,
        )

        await self.email_service.send_contact_notification(
            name=request.name,
            email=request.email,
            company=request.company or "N/A",
            phone=request.phone or "N/A",
            message=request.message,
        )

        return {
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "company": contact.company,
            "status": contact.status,
        }
