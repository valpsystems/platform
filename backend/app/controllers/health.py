from __future__ import annotations

from datetime import datetime, timezone

from app.core.config import settings
from app.utils.response import APIResponse


class HealthController:
    async def check(self) -> APIResponse:
        return APIResponse.success(
            data={
                "status": "healthy",
                "version": settings.APP_VERSION,
                "environment": settings.APP_ENV,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            message="Service is healthy")
