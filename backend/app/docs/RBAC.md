# Role-Based Access Control (RBAC)

## Overview

VALP SYSTEMS implements a comprehensive RBAC system with roles and permissions. The system uses:

- **Users**: Can be assigned multiple roles
- **Roles**: Groups of permissions; can be assigned to multiple users
- **Permissions**: Fine-grained access rights identified by unique codenames

## Database Schema

```
users ──< user_roles >── roles ──< role_permissions >── permissions
```

## Default Roles

- **admin**: Full system access (is_superuser)
- **user**: Standard authenticated user with basic permissions

## Permission Codename Convention

Permissions follow the convention: `<module>.<action>_<resource>`

Examples:
- `auth.read_user`
- `auth.update_user`
- `content.create_post`
- `content.delete_post`

## Usage in API Routes

### Require Authentication

```python
from app.api.dependencies.auth import get_current_active_user

@router.get("/protected")
async def protected_endpoint(
    current_user: dict = Depends(get_current_active_user),
):
    ...
```

### Require Specific Permissions

```python
from app.api.dependencies.auth import require_permissions

@router.post("/admin/users")
async def create_user(
    current_user: dict = Depends(require_permissions("auth.create_user")),
):
    ...

@router.delete("/admin/users/{id}")
async def delete_user(
    current_user: dict = Depends(require_permissions("auth.delete_user", "admin.access")),
):
    ...
```

### Require Specific Roles

```python
from app.api.dependencies.auth import require_roles

@router.post("/admin")
async def admin_only(
    current_user: dict = Depends(require_roles("admin")),
):
    ...
```

### Require Superuser

```python
from app.api.dependencies.auth import require_superuser

@router.post("/super-admin")
async def superuser_only(
    current_user: dict = Depends(require_superuser),
):
    ...
```

## Programmatic Permission Checks

```python
# In service or business logic
user.has_permission("content.create_post")
user.has_permissions("content.create_post", "content.publish_post")
user.has_role("admin")
```

## Superuser

- Superusers bypass all permission and role checks
- Set via `is_superuser` flag on the User model
- Only assignable through direct database manipulation or admin API

## Audit Logging

All auth-related actions are logged to the `audit_logs` table:
- User registration
- Login (successful and failed)
- Logout
- Token refresh
- Password changes
- Password reset requests
- Email verification
- Profile updates

## User Model Permissions Methods

```python
class User(Base):
    def has_role(self, role_name: str) -> bool: ...
    def has_permission(self, permission: str) -> bool: ...
    def has_permissions(self, *permissions: str) -> bool: ...
```
