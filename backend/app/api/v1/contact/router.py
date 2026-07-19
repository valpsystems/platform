from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import ContactController
from app.dependencies import get_db
from app.schemas.contact import ContactRequest, ContactResponse

router = APIRouter(
    prefix="/contact",
    tags=["Contact"],
)


@router.post(
    "",
    response_model=ContactResponse,
    summary="Submit Contact Request",
    description="Submit a contact request from the website contact form.",
)
async def submit_contact(
    request: ContactRequest,
    session: AsyncSession = Depends(get_db),
) -> ContactResponse:
    controller = ContactController(session)
    return await controller.submit(request)
