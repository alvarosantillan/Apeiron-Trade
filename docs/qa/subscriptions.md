# Subscriptions QA Report

## Feature

- `004-subscriptions`

## Environment

- Development container: `Apeiron-Trade` (Ubuntu via Docker Compose)
- Backend venv: `/app/backend/.venv`

## Executed Command

```bash
pytest tests/contract/subscriptions tests/integration/subscriptions tests/contract/auth tests/integration/auth tests/unit/auth -q
```

## Result

- Passed: 25
- Failed: 0
- Warnings: 1 (passlib deprecation warning)

## Covered Flows

- Checkout creation for paid plans
- Subscription status retrieval
- Webhook signature validation
- Webhook idempotent processing by `eventId`
- Approved/rejected payment state mapping (`active` / `past_due`)
- Plan transition endpoint (`free/plus/premium`)
- Cancellation endpoint (`cancelAtPeriodEnd` true/false)
- Auth regression suite included

## Notes

- Endpoints implemented under `/v1/subscriptions/*`.
- Current implementation uses in-memory stores suitable for early-stage development.
