# Runtime Deprecation Cleanup QA Report

## Feature

- `010-runtime-deprecation-cleanup`

## Scope

- Lifespan migration for FastAPI startup/shutdown wiring.
- Runtime warning policy handling without global warning suppression.
- Documentation and evidence for SC-001..SC-004.

## Baseline Comparison

### Pre-cleanup baseline

- Lifecycle deprecation warning observed during app startup (`@app.on_event("startup")`).
- Known dependency warnings observed intermittently in test runs.

### Post-cleanup baseline

- Lifecycle startup/shutdown now uses lifespan context manager.
- Lifecycle deprecation warnings: `0` in runtime-focused suites.
- Dependency warnings are classified with explicit treatment decisions.

## Evidence Matrix

| Success Criteria | Evidence |
|---|---|
| SC-001 | `backend/tests/integration/runtime/test_lifespan_no_deprecation.py` |
| SC-002 | Runtime contract/integration/unit suites passing |
| SC-003 | Warning decision matrix tests + scoped handling in `conftest.py` |
| SC-004 | `docs/methodology/runtime-warning-policy.md` + contract/quickstart references |

## Final Regression Commands

```bash
pytest tests/contract/runtime tests/integration/runtime tests/unit/validation -q
```

## Results

- Passed: Pending run
- Failed: Pending run
- Warnings: Pending run

## Notes

- No API route, payload, or business-flow contract changes were introduced in this feature.
