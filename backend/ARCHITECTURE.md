# Architecture Guide

## Clean Architecture Layers

```
┌─────────────────────────────────────────────┐
│              API Routes (api/v1/)            │
│     Define endpoints, wire to controllers    │
├─────────────────────────────────────────────┤
│              Controllers                     │
│     Orchestrate requests, validate auth      │
├─────────────────────────────────────────────┤
│              Services                        │
│     Business logic, multiple repos/emails    │
├─────────────────────────────────────────────┤
│              Repositories                    │
│     Data access, SQLAlchemy queries          │
├─────────────────────────────────────────────┤
│              Database / External             │
│     PostgreSQL, SMTP, Redis (future)         │
└─────────────────────────────────────────────┘
```

## Request Flow

1. HTTP request hits FastAPI
2. Middleware: Request ID → Logging → CORS → Error Handler → Security Headers
3. Router validates path/query params
4. Controller receives validated schema
5. Service executes business logic
6. Repository (optional) performs data operations
7. Service sends email (optional)
8. Controller returns APIResponse

## Directory Responsibilities

| Directory | Responsibility |
|---|---|
| `api/v1/` | Route definitions only — no business logic |
| `controllers/` | Request/response orchestration |
| `services/` | Business logic, calls repositories and external services |
| `repositories/` | Data access layer (Repository pattern) |
| `schemas/` | Pydantic v2 request/response models |
| `models/` | SQLAlchemy ORM models (Phase 4) |
| `database/` | Session management, engine, Base |
| `core/config/` | Environment-based configuration |
| `core/middleware/` | ASGI middleware components |
| `core/exceptions/` | Custom exception classes |
| `core/security/` | Hashing, JWT (Phase 5) |
| `emails/` | SMTP email service + Jinja2 templates |
| `utils/` | Logging, response helpers, datetime |

## Modular Monolith Design

The backend is a Modular Monolith — all code lives in one deployable unit but is organized into clear bounded contexts:

- Each API module (contact, newsletter, career, etc.) is independent
- Services are injectable and testable
- Database tables are organized by domain

### Migration to Microservices

When migrating to microservices:

1. Extract each API module into its own service
2. Move shared code to a common library
3. Replace direct service calls with HTTP/gRPC
4. Replace shared database with per-service databases
5. Add API gateway for routing
