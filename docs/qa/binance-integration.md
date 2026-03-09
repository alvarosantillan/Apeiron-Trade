# Binance Integration QA Report

## Feature

- `003-binance-integration`

## Environment

- Development container: `Apeiron-Trade` (Ubuntu via Docker)
- Backend venv: `/app/backend/.venv`

## Executed Commands

```bash
python -m pytest tests/contract/trading tests/integration/trading tests/unit/trading -q
python -m pytest -q
```

## Result

- Trading suite Passed: 10
- Full backend suite Passed: 35
- Failed: 0
- Warnings: 1 (passlib deprecation warning)

## Covered Flows

- Save Binance credentials for authenticated user
- Reject invalid credentials with `400`
- Fetch credential status with masked key suffix
- Execute real spot order successfully
- Handle insufficient balance without false success
- Enforce idempotency on duplicate `request_id`
- Enforce weekly real-operation limit by plan
- Allow paper trading when real weekly limit is exhausted
- Keep paper executions out of weekly real-operation counter

## Notes

- Trading endpoints implemented under `/v1/trading/*`.
- Current implementation uses in-memory stores for credentials, execution repository, idempotency, and weekly counters.
- Weekly limit values are resolved from `PlanBootstrapService` (`free=1`, `plus=10`, `premium=unlimited`).
