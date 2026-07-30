from __future__ import annotations
from typing import Optional


class AppException(Exception):
    def __init__(
        self,
        message: str = "An unexpected error occurred",
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[dict] = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details: Optional[dict] = None) -> None:
        super().__init__(message=message, error_code="NOT_FOUND", status_code=404, details=details)


class ValidationException(AppException):
    def __init__(self, message: str = "Validation failed", details: Optional[dict] = None) -> None:
        super().__init__(message=message, error_code="VALIDATION_ERROR", status_code=422, details=details)


class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists", details: Optional[dict] = None) -> None:
        super().__init__(message=message, error_code="CONFLICT", status_code=409, details=details)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Not authenticated", details: Optional[dict] = None) -> None:
        super().__init__(message=message, error_code="UNAUTHORIZED", status_code=401, details=details)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Permission denied", details: Optional[dict] = None) -> None:
        super().__init__(message=message, error_code="FORBIDDEN", status_code=403, details=details)


class RateLimitException(AppException):
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[dict] = None) -> None:
        super().__init__(message=message, error_code="RATE_LIMIT", status_code=429, details=details)


class ServiceUnavailableException(AppException):
    def __init__(self, message: str = "Service temporarily unavailable", details: Optional[dict] = None) -> None:
        super().__init__(message=message, error_code="SERVICE_UNAVAILABLE", status_code=503, details=details)