# Auth Baseline QA Report

## Feature

- `002-auth`

## Environment

- Development container: `Apeiron-Trade` (Ubuntu via Docker Compose)
- Backend virtual environment: `/app/backend/.venv`

## Executed Test Command

```bash
pytest tests/contract/auth tests/integration/auth tests/unit/auth -q
```

## Result

- Passed: 14
- Failed: 0
- Warnings: 1 (passlib deprecation warning from Python `crypt` module)

## Covered Flows

- Email registration and duplicate handling
- Email login success and invalid credentials
- Refresh token rotation and revocation behavior
- OAuth login (Google/Facebook) happy-path + invalid token
- Multi-session behavior with logout and logout-all
- Protected `GET /v1/users/me` with Bearer access token
- Access token claim integrity

## Notes

- Authentication routes are aligned with `specs/002-auth/contracts/auth.openapi.yaml` under `/v1`.
- Local development infrastructure file (`docker-compose.yml`) remains excluded from git tracking.
