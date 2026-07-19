from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.career_application import CareerApplicationRepository
from app.schemas.career import CareerRequest
from app.services import CareerService
from app.utils.response import APIResponse


class CareerController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = CareerService(CareerApplicationRepository(session))

    async def apply(self, request: CareerRequest) -> APIResponse:
        data = await self.service.process_application(request)
        return APIResponse.created(data=data, message="Application received successfully")
