from __future__ import annotations

from datetime import datetime, timezone
from collections.abc import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import RefreshToken
from app.repositories.base import BaseRepository
from typing import Optional


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RefreshToken, session)

    async def get_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        result = await self.session.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.is_deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def revoke(self, token_id: str) -> None:
        now = datetime.now(timezone.utc)
        await self.session.execute(
            update(RefreshToken)
            .where(RefreshToken.id == token_id)
            .values(is_revoked=True, revoked_at=now)
        )
        await self.session.flush()

    async def revoke_all_for_user(self, user_id: str) -> None:
        now = datetime.now(timezone.utc)
        await self.session.execute(
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
                RefreshToken.is_deleted.is_(False))
            .values(is_revoked=True, revoked_at=now)
        )
        await self.session.flush()

    async def get_valid_tokens_for_user(self, user_id: str) -> Sequence[RefreshToken]:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
                RefreshToken.expires_at > now,
                RefreshToken.is_deleted.is_(False))
        )
        return result.scalars().all()

    async def cleanup_expired(self) -> int:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.expires_at <= now)
        )
        expired = result.scalars().all()
        for token in expired:
            token.is_revoked = True
            token.revoked_at = now
        await self.session.flush()
        return len(expired)