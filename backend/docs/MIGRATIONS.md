# Migration Guide

## Setup

Initialize Alembic (already configured):

```bash
# The alembic directory is already set up at backend/alembic/
# alembic.ini is at backend/alembic.ini
```

## Creating Migrations

### Auto-generate from model changes

```bash
cd backend
alembic revision --autogenerate -m "description_of_changes"
```

This compares the current database schema with the SQLAlchemy models
and generates a migration file in `alembic/versions/`.

### Manual migration

```bash
cd backend
alembic revision -m "description_of_changes"
```

Edit the generated file in `alembic/versions/`.

## Applying Migrations

### Apply all pending migrations

```bash
cd backend
alembic upgrade head
```

### Apply one step

```bash
alembic upgrade +1
```

## Rolling Back

### Rollback one step

```bash
alembic downgrade -1
```

### Rollback to a specific revision

```bash
alembic downgrade <revision_id>
```

### Rollback all

```bash
alembic downgrade base
```

## Checking State

### Current revision

```bash
alembic current
```

### Migration history

```bash
alembic history
```

## Initial Migration

The initial migration (`0e9497533b08_initial.py`) creates all 9 tables:

1. contacts
2. newsletters
3. career_applications
4. quote_requests
5. feedbacks
6. technologies
7. services
8. solutions
9. resources

## Migration Workflow

1. **Modify models** in `app/models/`
2. **Generate migration** with `alembic revision --autogenerate`
3. **Review** the generated migration file
4. **Apply** with `alembic upgrade head`
5. **Test** with `pytest`

## Rules

- Never manually edit migration history
- Never delete migration files that have been applied
- Always review auto-generated migrations before applying
- Test migrations with `alembic upgrade head && alembic downgrade -1`
