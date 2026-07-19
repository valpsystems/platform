from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errorCode: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ValidationErrorResponse(BaseModel):
    success: bool = False
    message: str = "Validation failed"
    errorCode: str = "VALIDATION_ERROR"
    errors: list[dict] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
