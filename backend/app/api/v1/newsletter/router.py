from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import NewsletterController
from app.dependencies import get_db
from app.schemas.newsletter import NewsletterRequest, NewsletterResponse

router = APIRouter(
    prefix="/newsletter",
    tags=["Newsletter"],
)


@router.post(
    "",
    response_model=NewsletterResponse,
    summary="Subscribe to Newsletter",
    description="Subscribe an email address to the VALP SYSTEMS newsletter.",
)
async def subscribe_newsletter(
    request: NewsletterRequest,
    session: AsyncSession = Depends(get_db),
) -> NewsletterResponse:
    controller = NewsletterController(session)
    return await controller.subscribe(request)
