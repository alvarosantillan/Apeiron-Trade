# QA Evidence: Frontend Foundation (Sprint 011)

## Scope

- Feature: `011-frontend-foundation`
- Goal: P1 -> P2 -> P3 implementation over existing backend contracts
- Date: 2026-03-09

## Execution Notes

- TDD flow used where possible: tests authored before implementation for each story.
- Backend contract scope preserved (no new backend endpoints introduced).

## Test Evidence

### Unit

- Command (container): `docker exec Apeiron-Trade bash -lc 'cd /app/frontend; npm run test:run -- --reporter=dot'`
- Result:
	- `tests/unit/auth/session-store.test.tsx`
	- `tests/unit/ui/view-state-renderer.test.tsx`

### Integration

- Command (container): `docker exec Apeiron-Trade bash -lc 'cd /app/frontend; npm run test:run -- --reporter=dot'`
- Result: integration scope expanded and passing:
	- `tests/integration/auth/private-routes.test.tsx`
	- `tests/integration/auth/session-expiry-recovery.test.tsx`
	- `tests/integration/trading/trading-flow.test.tsx`
	- `tests/integration/dashboard/history-flow.test.tsx`
	- `tests/integration/notifications/notifications-flow.test.tsx`
	- `tests/integration/ai-agent/ai-config-flow.test.tsx`
	- `tests/integration/resilience/network-retry.test.tsx`

### E2E

- E2E spec scaffold created in `frontend/tests/e2e/us1-access-navigation.spec.ts`.
- E2E resilience scaffold created in `frontend/tests/e2e/us3-ux-reliability.spec.ts`.
- Execution pending browser runtime provisioning in container.

### Build Validation

- Command (container): `docker exec Apeiron-Trade bash -lc 'cd /app/frontend; npm run build'`
- Result: build successful (`vite build` completed)

### Current Test Totals

- Latest run (container): `9 files passed`, `13 tests passed`.

## Traceability (SC-001..SC-004)

- **SC-001**: Login + acceso dashboard validados por `tests/integration/auth/private-routes.test.tsx`.
- **SC-002**: Flujos core validados por `trading-flow`, `history-flow`, `notifications-flow`, `ai-config-flow`.
- **SC-003**: Guardas privadas y redireccion sin sesion verificadas en integration tests.
- **SC-004**: Mensajeria/normalizacion de errores validada por `session-expiry-recovery`, `network-retry` y `view-state-renderer`.

## Go/No-Go

- Current status: **Go for PR** (MVP baseline de Sprint 011 implementado y validado en unit/integration/build).
- Residual risk: E2E browser execution en contenedor pendiente de aprovisionamiento de browser runtime.

## Post-Merge Hotfix Notes

- Context: login web quedaba en `/login` tras autenticacion valida y el seed de demo se ejecutaba contra un destino distinto al runtime de API.
- Backend fix: habilitacion CORS para preflight en `POST /v1/auth/login` en `backend/src/main.py`.
- Frontend fix: redireccion de usuario autenticado fuera de `/login` y eliminacion de carrera de token provider en `frontend/src/app/main.tsx` y `frontend/src/pages/LoginPage.tsx`.
- Data fix: seeder alineado con `DBSettings` para usar la misma `DATABASE_URL` del runtime en `backend/scripts/seed_demo_data.py`.
- Validation: `docker exec Apeiron-Trade bash -lc 'cd /app/frontend; npm run test:run -- --reporter=dot'` y `docker exec Apeiron-Trade bash -lc 'cd /app/frontend; npm run build'` en verde.
