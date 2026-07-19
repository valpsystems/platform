# Database Architecture

## Technology

- **Database**: PostgreSQL 17+
- **ORM**: SQLAlchemy 2.0 (async + sync)
- **Migrations**: Alembic
- **Driver**: asyncpg (async), psycopg2 (sync)

## Connection Management

The database module (`app/database/`) provides:

- **Async Engine**: For async operations (FastAPI routes, services)
- **Sync Engine**: For Alembic migrations, scripts, and REPL
- **Session Factory**: `async_sessionmaker` / `sessionmaker`
- **Connection Pool**: Configurable pool size (default: 10), max overflow (default: 20)
- **Pool Pre-Ping**: Enabled for automatic connection health checks
- **Pool Recycle**: 3600 seconds (1 hour)

## Session Injection

FastAPI routes use a dependency-injected async session:

```python
from app.dependencies import get_db

@router.post("")
async def create(request: RequestSchema, session: AsyncSession = Depends(get_db)):
    ...
```

The session is auto-committed on success and rolled back on exception.

## Base Model

All models inherit from `app.database.base.Base`:

| Column | Type | Description |
|---|---|---|
| id | String(36) | UUID primary key |
| created_at | DateTime(tz) | Creation timestamp |
| updated_at | DateTime(tz) | Last update timestamp |
| created_by | String(36) | Creator user ID (future) |
| updated_by | String(36) | Last updater user ID (future) |
| is_active | Boolean | Active flag |
| is_deleted | Boolean | Soft delete flag |
| deleted_at | DateTime(tz) | Deletion timestamp |
| version | Integer | Optimistic locking |

## Database Health Check

The application performs a health check on startup:

```python
from app.database import check_database_health
health = await check_database_health()
```

## Shutdown

All database connections are properly disposed on application shutdown:

```python
from app.database import close_db_connections
await close_db_connections()
```

## Testing

In testing mode, the backend uses SQLite with aiosqlite driver.
All tables are created at test session start and dropped at session end.
Each test function gets an isolated session with automatic cleanup.

## Future Migrations

```bash
# Generate a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# Rollback to a specific revision
alembic downgrade <revision_id>

# View history
alembic history

# View current state
alembic current
```
