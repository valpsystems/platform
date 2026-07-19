# API Guidelines

## Base URL

All API endpoints are versioned under `/api/v1/`.

## Authentication

Authentication will be added in Phase 5. Currently all endpoints are public.

## Response Format

All endpoints return a consistent JSON envelope:

### Success Response (200/201)

```json
{
  "success": true,
  "message": "Human-readable message",
  "data": {},
  "timestamp": "2026-01-01T00:00:00Z"
}
```

### Error Response (4xx/5xx)

```json
{
  "success": false,
  "message": "Human-readable error",
  "errorCode": "ERROR_CODE",
  "timestamp": "2026-01-01T00:00:00Z"
}
```

## Error Codes

| Code | HTTP Status | Description |
|---|---|---|
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `CONFLICT` | 409 | Resource already exists |
| `UNAUTHORIZED` | 401 | Not authenticated |
| `FORBIDDEN` | 403 | Permission denied |
| `RATE_LIMIT` | 429 | Rate limit exceeded |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

## Request Headers

| Header | Required | Description |
|---|---|---|
| `Content-Type` | Yes | `application/json` |
| `X-Request-ID` | No | Client-provided request ID (UUID) |

## Rate Limiting

Rate limiting hooks are prepared but not yet active. Will be implemented in a future phase.

## Pagination

Pagination will follow this format when implemented:

```json
{
  "success": true,
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "pages": 5
  }
}
```

## Endpoint Conventions

- Use snake_case for request/response field names
- Use POST for all mutation endpoints
- Use GET for read-only endpoints
- Return 201 for resource creation
- Return 200 for successful operations
- Return 422 for validation errors
- Return 400 for bad requests (missing required fields)
