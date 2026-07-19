from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    success: bool = True
    message: str = "Service is healthy"
    data: dict = Field(
        default_factory=lambda: {
            "status": "healthy",
            "version": "1.0.0",
            "environment": "development",
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)
