from fastapi import APIRouter
from fastapi.responses import JSONResponse

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
async def health_check() -> JSONResponse:
    return await controller.check()
