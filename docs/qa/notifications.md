# Notifications QA Report

## Feature

- `007-notifications`

## Environment

- Development container: `Apeiron-Trade` (Ubuntu via Docker)
- Backend venv: `/app/backend/.venv`

## Executed Commands

```bash
python -m pytest tests/contract/notifications tests/integration/notifications -q
python -m pytest -q
```

## Result

- Notifications suite Passed: 7
- Full backend suite Passed: 60
- Failed: 0
- Warnings: 1 (passlib deprecation warning)

## Covered Flows

- Device token registration/update and listing
- Trading push event delivery for active devices
- Preference filtering by category
- Critical-priority override for disabled category
- Event deduplication per user/device/event
- Retry flow for transient push failures
- Invalid token drop with token deactivation

## Notes

- Device token responses never expose full `pushToken`.
- History endpoint supports limit and category filter.
- Delivery flow currently modeled with deterministic in-memory provider behavior for testability.
