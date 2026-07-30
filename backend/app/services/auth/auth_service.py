from __future__ import annotations

import hashlib
import secrets
from typing import Optional
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import JWTService, hash_password, verify_password
from app.emails import EmailService
from app.models.auth import User
from app.repositories.auth import (
    AuditLogRepository,
    LoginHistoryRepository,
    PermissionRepository,
    RefreshTokenRepository,
    RoleRepository,
    UserRepository)
from app.schemas.auth import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    UpdateProfileRequest)
from app.utils.logger import app_logger


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        role_repo: RoleRepository,
        permission_repo: PermissionRepository,
        refresh_token_repo: RefreshTokenRepository,
        audit_log_repo: AuditLogRepository,
        login_history_repo: LoginHistoryRepository) -> None:
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.permission_repo = permission_repo
        self.refresh_token_repo = refresh_token_repo
        self.audit_log_repo = audit_log_repo
        self.login_history_repo = login_history_repo
        self.email_service = EmailService()

    async def register(self, request: RegisterRequest, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> dict:
        existing_email = await self.user_repo.email_exists(request.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists")

        existing_username = await self.user_repo.username_exists(request.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This username is already taken")

        password_hash = hash_password(request.password)

        user = await self.user_repo.create(
            email=request.email,
            username=request.username,
            password_hash=password_hash,
            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone)

        default_role = await self.role_repo.get_by_name("user")
        if default_role:
            from app.models.auth import user_roles
            from sqlalchemy import insert
            from app.database.session import get_session
            stmt = insert(user_roles).values(
                user_id=user.id, role_id=default_role.id
            )
            await self.user_repo.session.execute(stmt)
            await self.user_repo.session.flush()

        verification = await self._create_email_verification(user)
        await self.email_service.send_verification_email(
            to_email=user.email,
            user_name=user.display_name(),
            token=verification.token)

        await self.audit_log_repo.create(
            actor_id=user.id,
            action="user.register",
            resource_type="user",
            resource_id=user.id,
            details=f"User registered: {user.email}",
            ip_address=ip_address,
            user_agent=user_agent)

        app_logger.info("User registered", user_id=user.id, email=user.email)

        return {
            "message": "Registration successful. Please check your email to verify your account.",
            "user": user.dict(),
            "requires_email_verification": True,
        }

    async def login(
        self,
        request: LoginRequest,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None) -> dict:
        user = await self.user_repo.get_by_email(request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password")

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated")

        if user.is_locked:
            if user.locked_until and datetime.now(timezone.utc) < user.locked_until:
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Account is temporarily locked. Try again later.")
            user.is_locked = False
            user.locked_until = None
            user.login_attempts = 0

        if not verify_password(request.password, user.password_hash):
            user.increment_login_attempts()
            if user.login_attempts >= 5:
                user.is_locked = True
                user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
            await self.user_repo.session.flush()

            await self.login_history_repo.create(
                user_id=user.id,
                login_at=datetime.now(timezone.utc),
                ip_address=ip_address,
                user_agent=user_agent,
                is_successful=False,
                failure_reason="Invalid password",
                auth_method="password")

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password")

        user.reset_login_attempts()
        user.last_login_at = datetime.now(timezone.utc)
        user.last_login_ip = ip_address

        access_expires = timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_expires = timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )

        if request.remember_me:
            refresh_expires = timedelta(days=30)

        access_token = JWTService.create_access_token(
            user_id=user.id,
            email=user.email,
            expires_delta=access_expires)

        refresh_token = JWTService.create_refresh_token(
            user_id=user.id,
            email=user.email,
            expires_delta=refresh_expires)

        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        refresh_expiry = datetime.now(timezone.utc) + refresh_expires

        await self.refresh_token_repo.create(
            token_hash=token_hash,
            user_id=user.id,
            expires_at=refresh_expiry,
            device_info=None,
            ip_address=ip_address,
            user_agent=user_agent)

        await self.login_history_repo.create(
            user_id=user.id,
            login_at=datetime.now(timezone.utc),
            ip_address=ip_address,
            user_agent=user_agent,
            is_successful=True,
            auth_method="password")

        await self.audit_log_repo.create(
            actor_id=user.id,
            action="user.login",
            resource_type="user",
            resource_id=user.id,
            details=f"User logged in: {user.email}",
            ip_address=ip_address,
            user_agent=user_agent)

        await self.user_repo.session.flush()

        user_data = user.dict()
        user_data["roles"] = [{"id": r.id, "name": r.name} for r in user.roles]

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": int(access_expires.total_seconds()),
            "user": user_data,
        }

    async def logout(self, user_id: str, refresh_token: Optional[str] = None) -> dict:
        if refresh_token:
            token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
            stored_token = await self.refresh_token_repo.get_by_token_hash(token_hash)
            if stored_token:
                await self.refresh_token_repo.revoke(stored_token.id)

        await self.refresh_token_repo.revoke_all_for_user(user_id)

        await self.audit_log_repo.create(
            actor_id=user_id,
            action="user.logout",
            resource_type="user",
            resource_id=user_id,
            details="User logged out")

        app_logger.info("User logged out", user_id=user_id)
        return {"message": "Logged out successfully"}

    async def refresh_token(
        self,
        refresh_token: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None) -> dict:
        payload = JWTService.decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token")

        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        stored_token = await self.refresh_token_repo.get_by_token_hash(token_hash)
        if not stored_token or not stored_token.is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked or expired")

        await self.refresh_token_repo.revoke(stored_token.id)

        user = await self.user_repo.get(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account not found or deactivated")

        access_expires = timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_expires = timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )

        new_access_token = JWTService.create_access_token(
            user_id=user.id,
            email=user.email,
            expires_delta=access_expires)

        new_refresh_token = JWTService.create_refresh_token(
            user_id=user.id,
            email=user.email,
            expires_delta=refresh_expires)

        new_token_hash = hashlib.sha256(new_refresh_token.encode()).hexdigest()
        await self.refresh_token_repo.create(
            token_hash=new_token_hash,
            user_id=user.id,
            expires_at=datetime.now(timezone.utc) + refresh_expires,
            ip_address=ip_address,
            user_agent=user_agent)

        await self.audit_log_repo.create(
            actor_id=user.id,
            action="user.token_refresh",
            resource_type="user",
            resource_id=user.id,
            details="Access token refreshed",
            ip_address=ip_address,
            user_agent=user_agent)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": int(access_expires.total_seconds()),
            "user": user.dict(),
        }

    async def get_profile(self, user_id: str) -> dict:
        user = await self.user_repo.get_with_roles(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")

        profile = user.dict()
        profile["roles"] = [r.name for r in user.roles]
        profile["permissions"] = list(set(
            perm.codename
            for role in user.roles
            for perm in role.permissions
        ))
        return profile

    async def update_profile(self, user_id: str, request: UpdateProfileRequest) -> dict:
        user = await self.user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")

        update_data = request.model_dump(exclude_none=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update")

        user = await self.user_repo.update(user_id, **update_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")

        await self.audit_log_repo.create(
            actor_id=user_id,
            action="user.profile_update",
            resource_type="user",
            resource_id=user_id,
            details=f"Profile updated fields: {', '.join(update_data.keys())}")

        return user.dict()

    async def change_password(
        self, user_id: str, request: ChangePasswordRequest
    ) -> dict:
        user = await self.user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")

        if not verify_password(request.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect")

        if request.current_password == request.new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from current password")

        new_hash = hash_password(request.new_password)
        await self.user_repo.update(
            user_id,
            password_hash=new_hash,
            password_changed_at=datetime.now(timezone.utc),
            require_password_change=False)

        await self.refresh_token_repo.revoke_all_for_user(user_id)

        try:
            await self.email_service.send_password_changed_email(
                to_email=user.email,
                user_name=user.display_name())
        except Exception as e:
            app_logger.warning("Failed to send password changed email", error=str(e))

        await self.audit_log_repo.create(
            actor_id=user_id,
            action="user.password_change",
            resource_type="user",
            resource_id=user_id,
            details="Password changed")

        return {"message": "Password changed successfully"}

    async def forgot_password(
        self,
        request: ForgotPasswordRequest,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None) -> dict:
        user = await self.user_repo.get_by_email(request.email)

        if not user:
            return {"message": "If the email exists, a password reset link has been sent"}

        from app.models.auth import PasswordReset as PasswordResetModel
        token = secrets.token_urlsafe(48)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(
            hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS
        )

        reset = PasswordResetModel(
            user_id=user.id,
            email=user.email,
            token=token_hash,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent)
        self.user_repo.session.add(reset)
        await self.user_repo.session.flush()

        try:
            await self.email_service.send_password_reset_email(
                to_email=user.email,
                user_name=user.display_name(),
                token=token,
                expires_hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
        except Exception as e:
            app_logger.error("Failed to send password reset email", error=str(e))

        await self.audit_log_repo.create(
            actor_id=user.id,
            action="user.forgot_password",
            resource_type="user",
            resource_id=user.id,
            details="Password reset requested",
            ip_address=ip_address,
            user_agent=user_agent)

        return {"message": "If the email exists, a password reset link has been sent"}

    async def reset_password(
        self,
        request: ResetPasswordRequest,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None) -> dict:
        from app.models.auth import PasswordReset as PasswordResetModel
        from sqlalchemy import select

        token_hash = hashlib.sha256(request.token.encode()).hexdigest()
        result = await self.user_repo.session.execute(
            select(PasswordResetModel).where(
                PasswordResetModel.token == token_hash,
                PasswordResetModel.is_used.is_(False),
                PasswordResetModel.is_deleted.is_(False))
        )
        reset_record = result.scalar_one_or_none()

        if not reset_record or reset_record.is_expired:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token")

        new_hash = hash_password(request.new_password)
        await self.user_repo.update(
            reset_record.user_id,
            password_hash=new_hash,
            password_changed_at=datetime.now(timezone.utc))

        reset_record.is_used = True
        reset_record.used_at = datetime.now(timezone.utc)
        reset_record.reset_at = datetime.now(timezone.utc)

        await self.refresh_token_repo.revoke_all_for_user(reset_record.user_id)

        await self.audit_log_repo.create(
            actor_id=reset_record.user_id,
            action="user.password_reset",
            resource_type="user",
            resource_id=reset_record.user_id,
            details="Password reset completed",
            ip_address=ip_address,
            user_agent=user_agent)

        await self.user_repo.session.flush()

        try:
            user = await self.user_repo.get(reset_record.user_id)
            if user:
                await self.email_service.send_password_reset_confirmation(
                    to_email=user.email,
                    user_name=user.display_name())
        except Exception as e:
            app_logger.warning("Failed to send reset confirmation email", error=str(e))

        return {"message": "Password has been reset successfully"}

    async def verify_email(self, token: str) -> dict:
        from app.models.auth import EmailVerification as EmailVerificationModel
        from sqlalchemy import select

        token_hash = hashlib.sha256(token.encode()).hexdigest()
        result = await self.user_repo.session.execute(
            select(EmailVerificationModel).where(
                EmailVerificationModel.token == token_hash,
                EmailVerificationModel.is_used.is_(False),
                EmailVerificationModel.is_deleted.is_(False))
        )
        verification = result.scalar_one_or_none()

        if not verification or verification.is_expired:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token")

        await self.user_repo.update(
            verification.user_id,
            is_email_verified=True)

        verification.is_used = True
        verification.used_at = datetime.now(timezone.utc)

        await self.audit_log_repo.create(
            actor_id=verification.user_id,
            action="user.email_verified",
            resource_type="user",
            resource_id=verification.user_id,
            details="Email verified")

        await self.user_repo.session.flush()

        return {"message": "Email verified successfully"}

    async def resend_verification(self, email: str) -> dict:
        user = await self.user_repo.get_by_email(email)
        if not user:
            return {"message": "If the email exists, a verification link has been sent"}

        if user.is_email_verified:
            return {"message": "Email is already verified"}

        verification = await self._create_email_verification(user)

        try:
            await self.email_service.send_verification_email(
                to_email=user.email,
                user_name=user.display_name(),
                token=verification.token)
        except Exception as e:
            app_logger.error("Failed to send verification email", error=str(e))

        return {"message": "If the email exists, a verification link has been sent"}

    async def _create_email_verification(self, user: User):
        from app.models.auth import EmailVerification as EmailVerificationModel

        token = secrets.token_urlsafe(48)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(
            hours=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS
        )

        verification = EmailVerificationModel(
            user_id=user.id,
            email=user.email,
            token=token_hash,
            expires_at=expires_at)
        self.user_repo.session.add(verification)
        await self.user_repo.session.flush()

        verification.token_plain = token
        return verification