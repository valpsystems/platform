# Security Guide

## Current Security Measures

### Middleware
- **CORS**: Restricted to configured origins
- **Trusted Hosts**: Only allowed hosts can connect
- **Security Headers**:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Strict-Transport-Security: max-age=31536000`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy: restricted defaults`
  - `Cache-Control: no-store, no-cache`

### Input Validation
- All inputs validated by Pydantic v2 schemas
- Email validation via `EmailStr`
- String length limits enforced
- Integer range validation (e.g., rating 1-5)

### Error Handling
- No stack traces exposed to clients
- Consistent error response format
- Internal errors return generic message

## Prepared for Future Phases

### Phase 5 — Authentication
- `app/core/security/` module ready
- Password hashing with SHA-256 + salt
- JWT token structure prepared
- Role-based access control design ready

### Environment
- Secret key required for production
- Database credentials via environment only
- SMTP credentials via environment only
- AWS credentials via environment only

## Security Checklist

- [ ] Change `APP_SECRET_KEY` in production
- [ ] Set `APP_DEBUG=false` in production
- [ ] Configure `CORS_ORIGINS` to specific domains
- [ ] Configure `TRUSTED_HOSTS` to specific hosts
- [ ] Use HTTPS in production
- [ ] Set strong database passwords
- [ ] Rotate SMTP credentials regularly
- [ ] Enable rate limiting (Phase 5)
- [ ] Add authentication (Phase 5)
