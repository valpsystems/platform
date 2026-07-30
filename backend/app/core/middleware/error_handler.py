from __future__ import annotations

from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.exceptions import AppException
from app.utils.logger import error_logger


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except AppException as exc:
            error_logger.error(
                "Application exception",
                error_code=exc.error_code,
                message=exc.message,
                status=exc.status_code,
                path=request.url.path,
                request_id=getattr(request.state, "request_id", None))
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "message": exc.message,
                    "errorCode": exc.error_code,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        except Exception:
            error_logger.exception(
                "Unhandled exception",
                path=request.url.path,
                request_id=getattr(request.state, "request_id", None))
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "An unexpected error occurred",
                    "errorCode": "INTERNAL_ERROR",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
