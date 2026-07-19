# Authentication & Authorization

## Overview

VALP SYSTEMS uses JWT-based authentication with access/refresh token rotation. The system supports:

- Email/password registration with email verification
- JWT access tokens (short-lived) + refresh tokens (long-lived)
- Password strength validation
- Account lockout after failed login attempts
- Email verification flow
- Forgot/reset password flow
- RBAC (Role-Based Access Control)

## Authentication Endpoints

All auth endpoints are prefixed with `/api/v1/auth`.

### Register
```
POST /api/v1/auth/register
```
Creates a new user account. Requires email verification via a confirmation link sent to the user's email.

### Login
```
POST /api/v1/auth/login
```
Returns `access_token` and `refresh_token`. Supports `remember_me` flag for extended sessions.

### Logout
```
POST /api/v1/auth/logout
```
Revokes all refresh tokens for the authenticated user.

### Refresh Token
```
POST /api/v1/auth/refresh
```
Exchanges a valid refresh token for new access + refresh tokens (token rotation).

### Get Profile
```
GET /api/v1/auth/me
```
Returns the authenticated user's profile with roles and permissions.

### Update Profile
```
PATCH /api/v1/auth/me
```
Updates profile fields (first_name, last_name, phone, bio, etc.).

### Change Password
```
POST /api/v1/auth/change-password
```
Changes the password for the authenticated user. Requires current password.

### Forgot Password
```
POST /api/v1/auth/forgot-password
```
Sends a password reset link to the user's registered email.

### Reset Password
```
POST /api/v1/auth/reset-password
```
Resets the password using a valid reset token.

### Verify Email
```
POST /api/v1/auth/verify-email
```
Verifies the user's email using a verification token.

### Resend Verification
```
POST /api/v1/auth/resend-verification
```
Resends the email verification link.

## Token Format

- **Access Token**: Short-lived JWT (default 30 minutes)
- **Refresh Token**: Long-lived JWT (default 7 days, 30 days with `remember_me`)
- **Token Type**: Bearer
- **Algorithm**: HS256

All tokens include a unique `jti` (JWT ID) claim to prevent hash collisions.

## Token Usage

Include the access token in the `Authorization` header:
```
Authorization: Bearer <access_token>
```

## Account Lockout

- After 5 failed login attempts, the account is locked for 15 minutes
- Login attempts reset on successful login
- Locked accounts cannot authenticate until the lock expires

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

Configure via environment variables:
- `PASSWORD_MIN_LENGTH` (default: 8)
- `PASSWORD_REQUIRE_UPPERCASE` (default: true)
- `PASSWORD_REQUIRE_LOWERCASE` (default: true)
- `PASSWORD_REQUIRE_DIGIT` (default: true)
- `PASSWORD_REQUIRE_SPECIAL` (default: false)

## JWT Configuration

Configure via environment variables:
- `JWT_SECRET_KEY`: Secret key for signing tokens
- `JWT_ALGORITHM`: Signing algorithm (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Access token TTL (default: 30)
- `JWT_REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token TTL (default: 7)

## Email Verification

- Verification token expires after 24 hours (configurable)
- Token is hashed before storage (SHA-256)
- Users must verify email before accessing protected resources if configured

## Password Reset

- Reset token expires after 1 hour (configurable)
- Token is hashed before storage (SHA-256)
- All refresh tokens are revoked after password reset
