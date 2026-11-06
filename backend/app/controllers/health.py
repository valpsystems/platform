from __future__ import annotations

from datetime import UTC, datetime

from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.response import APIResponse


class HealthController:
    async def check(self) -> JSONResponse:
        return APIResponse.success(
            data={
                "status": "healthy",
                "version": settings.APP_VERSION,
                "environment": settings.APP_ENV,
                "timestamp": datetime.now(UTC).isoformat(),
            },
            message="Service is healthy",
        )
