from fastapi import APIRouter

from app.controllers import HealthController
from app.schemas.health import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

controller = HealthController()


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns the health status of the application.",
)
async def health_check() -> HealthResponse:
    return await controller.check()
