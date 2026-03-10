# Constitution Exceptions

## Sprint 011 - Frontend Foundation MVP

**Date**: 2026-03-09
**Feature**: `011-frontend-foundation`
**Scope**: Web frontend MVP for TRDIA core user journeys.

## Context

Current constitution/frontend stack reference indicates React Native direction, while Sprint 011 requires a web MVP to validate existing backend features with real user flows.

## Exception Decision

- **Type**: Temporary stack exception
- **Approved direction for Sprint 011**: Web frontend MVP
- **Constraint**: No mobile-native implementation in this sprint
- **Constraint**: No backend contract expansion beyond existing endpoints from features `002` to `010`

## Rationale

- Backend capabilities are already available and validated.
- Product validation needs a usable web interface now.
- This exception minimizes time-to-feedback and preserves closed sprint scope.

## Guardrails

- Use this exception only for Sprint 011 deliverables.
- Reassess constitution alignment before Sprint 012 planning.
- Keep evidence and scope traceability in `specs/011-frontend-foundation/quickstart.md` and `docs/qa/frontend-foundation.md`.

## Approval Record

- **Approver**: Project Owner
- **Approval Status**: Approved
- **Approval Date**: 2026-03-09
- **Notes**: Proceed with web MVP for validation phase.

---

## Sprint 012 - Cryptocurrency UI Kit (Web Continuity)

**Date**: 2026-03-10
**Feature**: `012-cryptocurrency-ui-kit`
**Scope**: Visual integration of UI Kit for authenticated layout, Dashboard, and Trading.

## Revalidation Result

- **Type**: Stack continuity revalidation
- **Decision**: Keep approved web frontend direction for Sprint 012 under closed visual scope
- **Constraint**: No backend contract changes and no endpoint expansion
- **Constraint**: Preserve auth and private-route behavior from Sprint 011 baseline

## Approval Record

- **Approver**: Project Owner
- **Approval Status**: Approved
- **Approval Date**: 2026-03-10
- **Notes**: Governance gate cleared for Sprint 012 implementation using existing web stack.
