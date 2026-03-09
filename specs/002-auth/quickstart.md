# Quickstart - 002-auth

## Goal

Validate auth flows end-to-end in local dev.

## Preconditions

- Backend running
- PostgreSQL available
- OAuth test credentials configured

## Flows

1. Register (email/password)
- POST /v1/auth/register
- Expect 201 and user with plan=free

2. Login (email/password)
- POST /v1/auth/login
- Expect 200 with access_token + refresh_token

3. Access protected profile
- GET /v1/users/me with Bearer access_token
- Expect 200 and profile payload

4. Refresh session
- POST /v1/auth/refresh with refresh_token
- Expect 200 with new access_token + refresh_token
- Old refresh must become invalid

5. Logout
- POST /v1/auth/logout with refresh_token
- Expect 204
- Reusing same refresh must fail

6. Logout all sessions
- POST /v1/auth/logout-all with current refresh_token
- Expect 204
- Any refresh token previously issued for that user must fail

7. OAuth login
- POST /v1/auth/oauth/google or /v1/auth/oauth/facebook
- Expect 200 with internal JWT pair

## Negative checks

- Duplicate email registration -> 409
- Invalid credentials -> 401
- Expired/invalid refresh -> 401
- Excessive login attempts -> 429

## Validation Notes (2026-03-08)

- Contract + integration + unit tests validated in `Apeiron-Trade` container.
- Current result baseline: `14 passed` for auth suites.


