# Logging Guide

## Overview

Logging is handled by **Loguru** with four loggers:

| Logger | Tag | Purpose |
|---|---|---|
| `app_logger` | `type=app` | General application events |
| `access_logger` | `type=access` | HTTP request logging |
| `error_logger` | `type=error` | Exceptions and errors |
| `audit_logger` | `type=audit` | Audit trail (future) |

## Log Files

All logs are stored in `app/logs/`:

| File | Content | Retention |
|---|---|---|
| `app.log` | All logs (INFO+) | 30 days |
| `error.log` | ERROR+ level logs | 90 days |
| `access.log` | HTTP access logs | 30 days |

## Log Format

### JSON Format (default for production)

```json
{
  "timestamp": "2026-01-01T00:00:00.123",
  "level": "INFO",
  "module": "app.services.contact",
  "function": "process_contact",
  "line": 15,
  "message": "Processing contact request",
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Console Format (default for development)

```
2026-01-01 00:00:00.123 | INFO     | app.services.contact:process_contact:15 | Processing contact request
```

## Access Logging

Every HTTP request is logged by `RequestLoggingMiddleware` with:

- Request ID
- HTTP method
- Path
- Status code
- Execution time (ms)
- Environment

## Configuration

Configure logging via environment variables:

```
LOG_LEVEL=DEBUG            # DEBUG | INFO | WARNING | ERROR
LOG_FORMAT=json            # json | text
```

## Best Practices

1. Use structured logging — pass key=value pairs alongside the message
2. Use `app_logger.info()` for business events
3. Use `error_logger.exception()` for exceptions (includes traceback)
4. Never log sensitive data (passwords, tokens, PII)
5. Use `error_logger.error()` for application errors without traceback
