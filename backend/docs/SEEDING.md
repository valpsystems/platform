# Seeding Guide

## Overview

The seed module (`app/database/seed.py`) provides initial data for the application.

## Seed Data

### Services (5)

- Cloud Engineering
- Platform Engineering
- DevSecOps
- AI Engineering
- Managed Services

### Technologies (20)

Cloud (AWS, Azure, GCP), Containers (Kubernetes, Docker), IaC (Terraform, Ansible),
CI/CD (GitHub Actions, Jenkins), Languages (Python, TypeScript), Frontend (React),
Databases (PostgreSQL, Redis), Backend (FastAPI, Node.js), Monitoring (Prometheus, Grafana, Datadog, Elasticsearch)

### Solutions (6)

- Cloud Migration & Modernization
- CI/CD Pipeline Automation
- Kubernetes & Containerization
- Security & Compliance Automation
- AI/ML Platform Engineering
- Observability & Monitoring

### Resources (5)

- The Ultimate Guide to Cloud Migration Strategy
- Kubernetes Best Practices for Production
- DevSecOps: Integrating Security into Your Pipeline
- Building Internal Developer Platforms with Platform Engineering
- AI Engineering: From Experiment to Production

## Running Seeds

### From Python

```python
from app.database import get_async_session
from app.database.seed import seed_database

async def run_seed():
    async for session in get_async_session():
        await seed_database(session)

# Run:
# import asyncio
# asyncio.run(run_seed())
```

### Via script

```bash
cd backend
python -c "
import asyncio
from app.database.seed import seed_database
from app.database.session import async_session_factory

async def run():
    async with async_session_factory() as session:
        await seed_database(session)

asyncio.run(run())
"
```

## Idempotency

The seed script is idempotent — it checks if records already exist
before inserting. If a table already has data, seeding is skipped for that table.

## Clearing Data

```python
from app.database.seed import clear_database
# This deletes all data from all tables
```

## Development Workflow

1. Run migrations: `alembic upgrade head`
2. Seed data (once): run the seed script
3. Data persists for development sessions

## Adding New Seed Data

1. Add data constants to `app/database/seed.py`
2. Add insertion logic in `seed_database()` function
3. Run the seed script
