from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_active_user, get_current_user
from app.controllers.auth import AuthController
from app.dependencies import get_db
from app.schemas.auth import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenRefreshRequest,
    UpdateProfileRequest,
)
from app.schemas.auth.verify import ResendVerificationRequest, VerifyEmailRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    summary="Register a new user account",
    description="Creates a new user account with email verification requirement.",
)
async def register(
    request: Request,
    body: RegisterRequest,
    session: AsyncSession = Depends(get_db),
):
    controller = AuthController(session)
    return await controller.register(request, body)


@router.post(
    "/login",
    summary="Authenticate user and return tokens",
    description="Validates credentials and returns JWT access + refresh tokens.",
)
async def login(
    request: Request,
    body: LoginRequest,
    session: AsyncSession = Depends(get_db),
):
    controller = AuthController(session)
    return await controller.login(request, body)


@router.post(
    "/logout",
    summary="Logout user and revoke tokens",
    description="Revokes all refresh tokens for the authenticated user.",
)
async def logout(
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    controller = AuthController(session)
    return await controller.logout(current_user)


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Exchange a valid refresh token for new access + refresh tokens.",
)
async def refresh_token(
    request: Request,
    body: TokenRefreshRequest,
    session: AsyncSession = Depends(get_db),
):
    controller = AuthController(session)
    return await controller.refresh_token(request, body.refresh_token)


@router.get(
    "/me",
    summary="Get current user profile",
    description="Returns the authenticated user's profile with roles and permissions.",
)
async def get_profile(
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    controller = AuthController(session)
    return await controller.get_profile(current_user)


@router.patch(
    "/me",
    summary="Update current user profile",
    description="Updates the authenticated user's profile fields.",
)
async def update_profile(
    body: UpdateProfileRequest,
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    controller = AuthController(session)
    return await controller.update_profile(current_user, body)


@router.post(
    "/change-password",
    summary="Change current user password",
    description="Changes password for the authenticated user. Requires current password.",
)
async def change_password(
    body: ChangePasswordRequest,
    session: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    controller = AuthController(session)
    return await controller.change_password(current_user, body)


@router.post(
    "/forgot-password",
    summary="Request password reset email",
    description="Sends a password reset link to the user's registered email address.",
)
async def forgot_password(
    request: Request,
    body: ForgotPasswordRequest,
    session: AsyncSession = Depends(get_db),
):
    controller = AuthController(session)
    return await controller.forgot_password(request, body)


@router.post(
    "/reset-password",
    summary="Reset password with token",
    description="Resets the password using a valid reset token received via email.",
)
async def reset_password(
    request: Request,
    body: ResetPasswordRequest,
    session: AsyncSession = Depends(get_db),
):
    controller = AuthController(session)
    return await controller.reset_password(request, body)


@router.post(
    "/verify-email",
    summary="Verify email address",
    description="Verifies the user's email address using the verification token sent via email.",
)
async def verify_email(
    body: VerifyEmailRequest,
    session: AsyncSession = Depends(get_db),
):
    controller = AuthController(session)
    return await controller.verify_email(body)


@router.post(
    "/resend-verification",
    summary="Resend email verification link",
    description="Resends the email verification link to the user's email address.",
)
async def resend_verification(
    body: ResendVerificationRequest,
    session: AsyncSession = Depends(get_db),
):
    controller = AuthController(session)
    return await controller.resend_verification(body)
