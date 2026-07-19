from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import CareerController
from app.dependencies import get_db
from app.schemas.career import CareerRequest, CareerResponse

router = APIRouter(
    prefix="/careers",
    tags=["Careers"],
)


@router.post(
    "",
    response_model=CareerResponse,
    summary="Submit Job Application",
    description="Submit a job application through the careers page.",
)
async def apply_career(
    request: CareerRequest,
    session: AsyncSession = Depends(get_db),
) -> CareerResponse:
    controller = CareerController(session)
    return await controller.apply(request)
