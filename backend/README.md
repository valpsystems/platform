# VALP SYSTEMS — Backend API

**VALP SYSTEMS** Enterprise Backend API — a production-ready FastAPI backend built with Clean Architecture principles.

## Architecture

```
Request → API Routes → Controllers → Services → Repositories → Database
                                    ↘
                                Email Service
                                    ↘
                              External (SMTP)
```

The backend follows a **Modular Monolith** architecture, designed to allow seamless migration to microservices in future phases.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.13+ | Runtime |
| FastAPI | Web framework |
| Pydantic v2 | Validation & schemas |
| SQLAlchemy 2 | ORM (async + sync) |
| Alembic | Database migrations |
| Loguru | Structured logging |
| Jinja2 | Email templating |
| Uvicorn | ASGI server |
| Pytest | Testing |

## Project Structure

```
backend/
├── app/
│   ├── api/v1/           # API route modules
│   │   ├── health/       # GET /api/v1/health
│   │   ├── contact/      # POST /api/v1/contact
│   │   ├── newsletter/   # POST /api/v1/newsletter
│   │   ├── careers/      # POST /api/v1/careers
│   │   ├── quote/        # POST /api/v1/quote
│   │   └── feedback/     # POST /api/v1/feedback
│   ├── controllers/      # Request orchestration
│   ├── services/         # Business logic
│   ├── repositories/     # Data access (Repository pattern)
│   ├── schemas/          # Pydantic request/response models
│   ├── models/           # SQLAlchemy models (Phase 4)
│   ├── database/         # Session management, Base model
│   ├── core/             # Config, middleware, exceptions, security
│   ├── emails/           # Email service & templates
│   ├── utils/            # Logger, response helpers
│   └── constants/        # Application constants
├── tests/                # Pytest test suite
├── scripts/              # Utility scripts
├── docs/                 # Documentation
├── pyproject.toml        # Project config
├── requirements.txt      # Dependencies
└── .env.example          # Environment template
```

## Quick Start

```bash
# Requirements
Python 3.13+
pip install -r requirements.txt

# Environment
cp .env.example .env
# Edit .env with your settings

# Run (development)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the script
.\scripts\run.ps1 dev   # PowerShell
./scripts/run.sh dev     # Bash

# Run (production)
.\scripts\run.ps1 prod
```

## API Documentation

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/health` | GET | Health check |
| `/api/v1/auth/register` | POST | Register a new user |
| `/api/v1/auth/login` | POST | Authenticate and get tokens |
| `/api/v1/auth/logout` | POST | Revoke refresh tokens |
| `/api/v1/auth/refresh` | POST | Refresh access token |
| `/api/v1/auth/me` | GET | Get current user profile |
| `/api/v1/auth/me` | PATCH | Update profile |
| `/api/v1/auth/change-password` | POST | Change password |
| `/api/v1/auth/forgot-password` | POST | Request password reset |
| `/api/v1/auth/reset-password` | POST | Reset password with token |
| `/api/v1/auth/verify-email` | POST | Verify email address |
| `/api/v1/auth/resend-verification` | POST | Resend verification email |
| `/api/v1/contact` | POST | Submit contact form |
| `/api/v1/newsletter` | POST | Subscribe to newsletter |
| `/api/v1/careers` | POST | Submit job application |
| `/api/v1/quote` | POST | Request a quote |
| `/api/v1/feedback` | POST | Submit feedback |

Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`

## Documentation

| Document | Description |
|---|---|
| [DEPLOYMENT](./app/docs/DEPLOYMENT.md) | Local dev + EC2 prod deployment (step-by-step) |
| [AUTHENTICATION](./app/docs/AUTHENTICATION.md) | JWT auth, tokens, password policy |
| [RBAC](./app/docs/RBAC.md) | Roles, permissions, access control |

## API Response Format

**Success:**
```json
{
  "success": true,
  "message": "Contact request received successfully",
  "data": { "name": "John Doe", "email": "john@example.com" },
  "timestamp": "2026-01-01T00:00:00Z"
}
```

**Error:**
```json
{
  "success": false,
  "message": "Validation failed",
  "errorCode": "VALIDATION_ERROR",
  "timestamp": "2026-01-01T00:00:00Z"
}
```

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=app/        # With coverage
pytest tests/ -v --log-cli-level=INFO
```

## Verification Status

- ✅ FastAPI application starts successfully
- ✅ All 17 API endpoints functional (6 public + 11 auth)
- ✅ Pydantic v2 validation on all inputs
- ✅ Enterprise response format (consistent success/error)
- ✅ OpenAPI/Swagger/ReDoc documentation
- ✅ Ruff linting passes (0 errors)
- ✅ Pytest: 46 tests passing (20 auth + 26 existing)
- ✅ Middleware: Request ID, logging, CORS, security headers, error handling
- ✅ Loguru structured logging to file and console
- ✅ Email infrastructure with Jinja2 templates
- ✅ Database: 19 tables (9 business + 10 auth)
- ✅ Authentication: JWT access/refresh tokens with rotation
- ✅ Authorization: RBAC with roles, permissions, and superuser
- ✅ Security: bcrypt hashing, account lockout, password strength validation
- ✅ Deployment: Local (SQLite) + EC2 (PostgreSQL) documented
