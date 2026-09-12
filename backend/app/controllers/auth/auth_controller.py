from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.auth import (
    AuditLogRepository,
    LoginHistoryRepository,
    PermissionRepository,
    RefreshTokenRepository,
    RoleRepository,
    UserRepository,
)
from app.schemas.auth import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    UpdateProfileRequest,
)
from app.schemas.auth.verify import ResendVerificationRequest, VerifyEmailRequest
from app.services.auth import AuthService
from app.utils.response import APIResponse


class AuthController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = AuthService(
            user_repo=UserRepository(session),
            role_repo=RoleRepository(session),
            permission_repo=PermissionRepository(session),
            refresh_token_repo=RefreshTokenRepository(session),
            audit_log_repo=AuditLogRepository(session),
            login_history_repo=LoginHistoryRepository(session),
        )
        self.session = session

    async def register(
        self,
        request: Request,
        body: RegisterRequest,
    ) -> JSONResponse:
        result = await self.service.register(
            request=body,
            ip_address=self._get_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
        return APIResponse.created(data=result, message=result["message"])

    async def login(
        self,
        request: Request,
        body: LoginRequest,
    ) -> JSONResponse:
        result = await self.service.login(
            request=body,
            ip_address=self._get_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
        return APIResponse.success(data=result, message="Login successful")

    async def logout(
        self,
        current_user: dict,
        refresh_token: str | None = None,
    ) -> JSONResponse:
        result = await self.service.logout(
            user_id=current_user["id"],
            refresh_token=refresh_token,
        )
        return APIResponse.success(message=result["message"])

    async def refresh_token(
        self,
        request: Request,
        refresh_token: str,
    ) -> JSONResponse:
        result = await self.service.refresh_token(
            refresh_token=refresh_token,
            ip_address=self._get_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
        return APIResponse.success(data=result, message="Token refreshed")

    async def get_profile(
        self,
        current_user: dict,
    ) -> JSONResponse:
        profile = await self.service.get_profile(user_id=current_user["id"])
        return APIResponse.success(data=profile, message="Profile retrieved")

    async def update_profile(
        self,
        current_user: dict,
        body: UpdateProfileRequest,
    ) -> JSONResponse:
        result = await self.service.update_profile(
            user_id=current_user["id"],
            request=body,
        )
        return APIResponse.success(data=result, message="Profile updated")

    async def change_password(
        self,
        current_user: dict,
        body: ChangePasswordRequest,
    ) -> JSONResponse:
        result = await self.service.change_password(
            user_id=current_user["id"],
            request=body,
        )
        return APIResponse.success(message=result["message"])

    async def forgot_password(
        self,
        request: Request,
        body: ForgotPasswordRequest,
    ) -> JSONResponse:
        result = await self.service.forgot_password(
            request=body,
            ip_address=self._get_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
        return APIResponse.success(message=result["message"])

    async def reset_password(
        self,
        request: Request,
        body: ResetPasswordRequest,
    ) -> JSONResponse:
        result = await self.service.reset_password(
            request=body,
            ip_address=self._get_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
        return APIResponse.success(message=result["message"])

    async def verify_email(
        self,
        body: VerifyEmailRequest,
    ) -> JSONResponse:
        result = await self.service.verify_email(token=body.token)
        return APIResponse.success(message=result["message"])

    async def resend_verification(
        self,
        body: ResendVerificationRequest,
    ) -> JSONResponse:
        result = await self.service.resend_verification(email=body.email)
        return APIResponse.success(message=result["message"])

    def _get_ip(self, request: Request) -> str | None:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else None
