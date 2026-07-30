from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Header, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.core.security import JWTService
from app.repositories.auth import UserRepository

security_scheme = HTTPBearer(auto_error=False)


async def get_token_from_header(
    authorization: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security_scheme)] = None,
    x_api_key: Annotated[Optional[str], Header()] = None,
) -> Optional[str]:
    if authorization:
        return authorization.credentials
    if x_api_key:
        return x_api_key
    return None


async def get_current_user(
    token: Annotated[Optional[str], Depends(get_token_from_header)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = JWTService.decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_repo = UserRepository(session)
    user = await user_repo.get_with_roles(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated",
        )

    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account is locked",
        )

    user_data = user.dict()
    user_data["roles"] = [{"id": r.id, "name": r.name} for r in user.roles]
    user_data["permissions"] = list(set(
        perm.codename
        for role in user.roles
        for perm in role.permissions
    ))
    return user_data


async def get_current_active_user(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    if not current_user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


class PermissionChecker:
    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

    async def __call__(
        self,
        current_user: Annotated[dict, Depends(get_current_active_user)],
    ) -> dict:
        if current_user.get("is_superuser"):
            return current_user

        user_permissions = set(current_user.get("permissions", []))
        missing = [
            p for p in self.required_permissions if p not in user_permissions
        ]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {', '.join(missing)}",
            )
        return current_user


class RoleChecker:
    def __init__(self, required_roles: list[str]) -> None:
        self.required_roles = required_roles

    async def __call__(
        self,
        current_user: Annotated[dict, Depends(get_current_active_user)],
    ) -> dict:
        if current_user.get("is_superuser"):
            return current_user

        user_roles = {r["name"] for r in current_user.get("roles", [])}
        missing = [r for r in self.required_roles if r not in user_roles]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required roles: {', '.join(missing)}",
            )
        return current_user


def require_permissions(*permissions: str) -> PermissionChecker:
    return PermissionChecker(list(permissions))


def require_roles(*roles: str) -> RoleChecker:
    return RoleChecker(list(roles))


async def require_superuser(
    current_user: Annotated[dict, Depends(get_current_active_user)],
) -> dict:
    if not current_user.get("is_superuser"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser access required",
        )
    return current_user
