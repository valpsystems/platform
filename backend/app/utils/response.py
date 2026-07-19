from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse


class APIResponse:
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": data,
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

    @staticmethod
    def created(data: Any = None, message: str = "Created successfully") -> JSONResponse:
        return APIResponse.success(data=data, message=message, status_code=status.HTTP_201_CREATED)

    @staticmethod
    def error(
        message: str = "An error occurred",
        error_code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "errorCode": error_code,
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

    @staticmethod
    def validation_error(message: str = "Validation failed") -> JSONResponse:
        return APIResponse.error(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
