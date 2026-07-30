from __future__ import annotations

from typing import Any, Optional

from app.repositories.auth import AuditLogRepository


class AuditService:
    def __init__(self, audit_log_repo: AuditLogRepository) -> None:
        self.audit_log_repo = audit_log_repo

    async def log(
        self,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        details: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_method: Optional[str] = None,
        request_path: Optional[str] = None,
        status_code: Optional[int] = None,
        duration_ms: Optional[int] = None,
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