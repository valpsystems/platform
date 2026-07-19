# Changelog

## [1.0.0] — 2026-07-19

### Added
- FastAPI project with Clean Architecture
- 6 API endpoints: Health, Contact, Newsletter, Career, Quote, Feedback
- Enterprise response format (consistent success/error JSON)
- Pydantic v2 validation on all request/response schemas
- SQLAlchemy 2 async/sync engine configuration
- Alembic migration infrastructure (prepared)
- Loguru logging (app, access, error, audit)
- Middleware: Request ID, Logging, CORS, Error Handler, Security Headers
- Custom exception hierarchy with error codes
- Email service with Jinja2 templates (Contact, Newsletter, Career, Quote, Feedback)
- Repository pattern for data access
- Password hashing utilities (prepared)
- `.env.example` configuration template
- Project documentation: README, ARCHITECTURE, API_GUIDELINES, LOGGING, SECURITY, ROADMAP, CHANGELOG
- Pytest test suite (7 tests)
- Ruff linting configuration

### Architecture
- Modular monolith — prepared for microservices migration
- Clean Architecture layers: Routes → Controllers → Services → Repositories → Database
- All business logic in Services layer
- All request/response handling in Controllers
- All route definitions in api/v1/ modules
