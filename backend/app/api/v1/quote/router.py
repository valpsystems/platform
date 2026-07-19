from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import QuoteController
from app.dependencies import get_db
from app.schemas.quote import QuoteRequest, QuoteResponse

router = APIRouter(
    prefix="/quote",
    tags=["Quote"],
)


@router.post(
    "",
    response_model=QuoteResponse,
    summary="Request a Quote",
    description="Submit a quote request for enterprise services.",
)
async def request_quote(
    quote_request: QuoteRequest,
    session: AsyncSession = Depends(get_db),
) -> QuoteResponse:
    controller = QuoteController(session)
    return await controller.request(quote_request)
