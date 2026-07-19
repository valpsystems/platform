from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import FeedbackController
from app.dependencies import get_db
from app.schemas.feedback import FeedbackRequest, FeedbackResponse

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@router.post(
    "",
    response_model=FeedbackResponse,
    summary="Submit Feedback",
    description="Submit feedback about VALP SYSTEMS services.",
)
async def submit_feedback(
    request: FeedbackRequest,
    session: AsyncSession = Depends(get_db),
) -> FeedbackResponse:
    controller = FeedbackController(session)
    return await controller.submit(request)
