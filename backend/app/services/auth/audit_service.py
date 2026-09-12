from __future__ import annotations

from typing import Any

from app.repositories.auth import AuditLogRepository


class AuditService:
    def __init__(self, audit_log_repo: AuditLogRepository) -> None:
        self.audit_log_repo = audit_log_repo

    async def log(
        self,
        action: str,
        resource_type: str,
        resource_id: str | None = None,
        actor_id: str | None = None,
        details: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        request_method: str | None = None,
        request_path: str | None = None,
        status_code: int | None = None,
        duration_ms: int | None = None,
    ) -> dict[str, Any]:
        audit = await self.audit_log_repo.create(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            actor_id=actor_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            request_method=request_method,
            request_path=request_path,
            status_code=status_code,
            duration_ms=duration_ms,
        )
        return audit.dict()
