from __future__ import annotations

from datetime import UTC, datetime

from app.core.config import settings
from app.utils.response import APIResponse


class HealthController:
    async def check(self) -> APIResponse:
        return APIResponse.success(
            data={
                "status": "healthy",
                "version": settings.APP_VERSION,
                "environment": settings.APP_ENV,
                "timestamp": datetime.now(UTC).isoformat(),
            },
            message="Service is healthy",
        )
