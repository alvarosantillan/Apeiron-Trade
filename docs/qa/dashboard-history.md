# Dashboard and History QA Report

## Feature

- `008-dashboard-history`

## Environment

- Development container: `Apeiron-Trade` (Ubuntu via Docker)
- Backend venv: `/app/backend/.venv`

## Executed Commands

```bash
python -m pytest tests/contract/dashboard_history tests/integration/dashboard_history -q
python -m pytest -q
```

## Result

- Dashboard/history suite Passed: 8
- Full backend suite Passed: 68
- Failed: 0
- Warnings: 1 (passlib deprecation warning)

## Covered Flows

- Dashboard summary for active and new users
- Trade history listing with filters and cursor pagination
- Trade detail retrieval with audit access logging
- KPI aggregates for `7d` and `30d` windows
- Validation error on unsupported KPI window

## Notes

- Dashboard values are composed from current plan, weekly counter and bot status.
- Trade history and detail are sourced from execution repository records.
- Trade detail endpoint writes an audit event per access.
