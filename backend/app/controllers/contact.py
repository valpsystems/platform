from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.contact import ContactRepository
from app.schemas.contact import ContactRequest
from app.services import ContactService
from app.utils.response import APIResponse


class ContactController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = ContactService(ContactRepository(session))

    async def submit(self, request: ContactRequest) -> APIResponse:
        data = await self.service.process_contact(request)
        return APIResponse.created(data=data, message="Contact request received successfully")
