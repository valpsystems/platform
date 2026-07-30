from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


class JWTService:
    @staticmethod
    def _generate_jti() -> str:
        return secrets.token_urlsafe(16)

    @staticmethod
    def create_access_token(
        user_id: str,
        email: str,
        extra_claims: dict | None = None,
        expires_delta: timedelta | None = None) -> str:
        expires_in = expires_delta or timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        now = datetime.now(timezone.utc)
        payload = {
            "jti": JWTService._generate_jti(),
            "sub": user_id,
            "email": email,
            "type": "access",
            "iat": now,
            "exp": now + expires_in,
        }
        if extra_claims:
            payload.update(extra_claims)
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(
        user_id: str,
        email: str,
        expires_delta: timedelta | None = None) -> str:
        expires_in = expires_delta or timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )
        now = datetime.now(timezone.utc)
        payload = {
            "jti": JWTService._generate_jti(),
            "sub": user_id,
            "email": email,
            "type": "refresh",
            "iat": now,
            "exp": now + expires_in,
        }
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict | None:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def get_token_expiry(token: str) -> int:
        payload = JWTService.decode_token(token)
        if payload is None or "exp" not in payload:
            return 0
        return payload["exp"]

    @staticmethod
    def is_token_expired(token: str) -> bool:
        payload = JWTService.decode_token(token)
        if payload is None:
            return True
        exp = payload.get("exp", 0)
        return datetime.now(timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc)

    @staticmethod
    def get_token_type(token: str) -> str | None:
        payload = JWTService.decode_token(token)
        if payload is None:
            return None
        return payload.get("type")

    @staticmethod
    def get_user_id_from_token(token: str) -> str | None:
        payload = JWTService.decode_token(token)
        if payload is None:
            return None
        return payload.get("sub")
