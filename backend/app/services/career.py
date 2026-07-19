from __future__ import annotations

from app.constants.enums import ApplicationStatus
from app.emails import EmailService
from app.repositories.career_application import CareerApplicationRepository
from app.schemas.career import CareerRequest
from app.utils.logger import app_logger


class CareerService:
    def __init__(self, repository: CareerApplicationRepository) -> None:
        self.repository = repository
        self.email_service = EmailService()

    async def process_application(self, request: CareerRequest) -> dict:
        app_logger.info(
            "Processing career application",
            name=request.name,
            email=request.email,
            position=request.position,
        )

        application = await self.repository.create(
            name=request.name,
            email=request.email,
            phone=request.phone,
            position=request.position,
            experience_years=request.experience_years,
            cover_letter=request.cover_letter,
            linkedin_url=request.linkedin_url,
            portfolio_url=request.portfolio_url,
            status=ApplicationStatus.PENDING,
        )

        await self.email_service.send_career_application(
            name=request.name,
            email=request.email,
            position=request.position,
            phone=request.phone or "N/A",
            experience_years=request.experience_years,
            cover_letter=request.cover_letter or "N/A",
            linkedin_url=request.linkedin_url or "N/A",
            portfolio_url=request.portfolio_url or "N/A",
        )

        return {
            "id": application.id,
            "name": application.name,
            "email": application.email,
            "position": application.position,
            "status": application.status,
        }
