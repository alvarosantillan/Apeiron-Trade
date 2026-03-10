# QA Evidence: Cryptocurrency UI Kit (Sprint 012)

## Scope

- Feature: `012-cryptocurrency-ui-kit`
- Iteration scope: authenticated layout + dashboard + trading
- Out of scope: backend contracts, endpoint behavior, business validation rules

## Baseline Snapshot

- Baseline date: 2026-03-10
- Baseline private routes: `/dashboard`, `/trading`, `/notifications`, `/ai-agent`
- Baseline auth behavior:
  - Unauthenticated access to private routes redirects to `/login`
  - Authenticated access renders private area

## FR/SC Traceability Matrix

| Spec Item | Validation Layer | Test/Evidence |
|-----------|------------------|---------------|
| FR-001 | Unit + Integration + E2E | `private-layout.test.tsx`, `private-routes.test.tsx`, `us1-access-navigation.spec.ts` |
| FR-002 | Integration | `private-routes.test.tsx` |
| FR-003 | Unit + Integration + E2E | `view-state-renderer.test.tsx`, `history-flow.test.tsx`, `us2-dashboard-ui-kit.spec.ts` |
| FR-004 | Unit + Integration + E2E | `trading-form-state.test.tsx`, `trading-flow.test.tsx`, `us3-ux-reliability.spec.ts` |
| FR-005 | Unit + Integration | `view-state-renderer.test.tsx`, dashboard/trading page state assertions |
| FR-006 | Manual responsive checklist | Section "Responsive and Accessibility" |
| FR-007 | Unit + Manual keyboard/focus | `private-layout.test.tsx` + manual checklist |
| FR-008 | Regression suite | Section "Regression Results" |
| FR-010 | Contract freeze validation | Section "Backend Contract Validation" |
| SC-001 | Integration + E2E smoke | `private-routes.test.tsx`, `us1-access-navigation.spec.ts` |
| SC-004 | Regression suite | Section "Regression Results" |

## Regression Results

- Execution mode: container-first (`Apeiron-Trade`)
- Frontend unit/integration status: PASS
  - Command: `docker exec Apeiron-Trade bash -lc "cd /app/frontend && npm run test:run -- --reporter=dot"`
  - Result: `11 passed files`, `15 passed tests`
- Frontend build status: PASS
  - Command: `docker exec Apeiron-Trade bash -lc "cd /app/frontend && npm run build"`
  - Result: `tsc -b && vite build` completado, bundle generado en `dist/`
- E2E smoke status: PASS (tras instalar dependencias de runtime)
  - Initial blocker: faltaban binario Chromium y librerias del sistema (`libnspr4.so`)
  - Commands:
    - `docker exec Apeiron-Trade bash -lc "cd /app/frontend && npx playwright install chromium"`
    - `docker exec Apeiron-Trade bash -lc "cd /app/frontend && npx playwright install-deps chromium"`
    - `docker exec Apeiron-Trade bash -lc "cd /app/frontend && npx playwright test tests/e2e/us1-access-navigation.spec.ts tests/e2e/us2-dashboard-ui-kit.spec.ts tests/e2e/us3-ux-reliability.spec.ts --reporter=dot"`
  - Result: `5 passed (10.8s)`

## Responsive and Accessibility

- Viewports validated:
  - Desktop: PASS (`1366x768`) en `/dashboard` y `/trading`
  - Mobile: PASS (`390x844`) en `/dashboard` y `/trading`
- Accessibility baseline:
  - Focus visible in private navigation: PASS (outline `auto` 1px en secuencia TAB)
  - Keyboard access for private navigation links: PASS (TAB recorre `Dashboard -> Trading -> Notifications -> AI Agent`)
  - Contrast in authenticated shell cards/navigation: PASS para pares de texto principales
    - `textPrimary` sobre `pageBg`: 17.42
    - `textOnDark` sobre `shellBg`: 17.06
    - `textMuted` sobre `panelBg`: 7.56
  - Nota: `accent` sobre `panelBg` es 2.77; mantener uso decorativo/no textual para conservar legibilidad AA.

## Backend Contract Validation

- Result: No backend changes in Sprint 012 implementation.
- Verified areas:
  - No cambios detectados en endpoints/contratos de `backend/src/api`
  - No new frontend API endpoint paths introduced
  - Existing dashboard and trading API contracts reused

## Notes

- This document is updated progressively as command evidence is produced.
- Nota de entorno: para ejecutar smoke E2E en este contenedor fue necesario instalar runtime de Playwright (browser + system deps).
- Evidencia responsive/keyboard ejecutada via Playwright script ad-hoc contra `http://127.0.0.1:5173` en contenedor.
