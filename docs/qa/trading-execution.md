# Trading Execution QA Report

## Feature

- `006-trading-execution`

## Environment

- Development container: `Apeiron-Trade` (Ubuntu via Docker)
- Backend venv: `/app/backend/.venv`

## Executed Commands

```bash
python -m pytest tests/contract/trading_execution tests/integration/trading_execution -q
python -m pytest -q
```

## Result

- Trading execution suite Passed: 7
- Full backend suite Passed: 52
- Failed: 0
- Warnings: 1 (passlib deprecation warning)

## Covered Flows

- Create validated real execution (`201`, status terminal)
- Block by weekly plan limit with `blockedReason=weekly_limit_exceeded`
- Block by insufficient balance with `blockedReason=insufficient_balance`
- Keep paper execution outside weekly real counter
- Enforce idempotent behavior by `requestId`
- Handle timeout path with `PENDING_RECONCILIATION` and reconciliation worker completion

## Notes

- Endpoints implemented under `/v1/trading/executions`.
- Legacy `/v1/trading/execute` endpoint remains available for previous feature compatibility.
- Reconciliation worker currently resolves pending states deterministically for integration tests.
