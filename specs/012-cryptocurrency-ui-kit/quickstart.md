# Quickstart: Cryptocurrency UI Kit Integration (Iteracion 1)

## Objective

Confirmar readiness de la feature 012 para ejecutar `/speckit.tasks` con alcance cerrado: layout autenticado + Dashboard + Trading, sin cambios de backend y sin regresiones en flujos existentes.

## Prerequisites

- Artefactos de planificacion completados:
  - `specs/012-cryptocurrency-ui-kit/spec.md`
  - `specs/012-cryptocurrency-ui-kit/plan.md`
  - `specs/012-cryptocurrency-ui-kit/research.md`
  - `specs/012-cryptocurrency-ui-kit/data-model.md`
  - `specs/012-cryptocurrency-ui-kit/contracts/frontend-ui-kit-integration.md`
- Baseline frontend de Sprint 011 vigente y en verde en pruebas existentes.

## Readiness Flow

1. Verificar que historias P1-P3 se mantienen en alcance visual (sin cambios de negocio).
2. Confirmar que layout autenticado conserva guardas y redirecciones actuales.
3. Confirmar contrato de estados UX (`loading/empty/error/success`) para Dashboard y Trading.
4. Verificar que no hay cambios requeridos en endpoints, payloads o validaciones backend.
5. Registrar pendiente de governance de stack (revalidacion post-excepcion Sprint 011) antes de implementar.

## Scenario 1: Layout Autenticado (P1)

1. Revisar definicion de `AuthenticatedLayoutState` y componentes UI Kit previstos.
2. Confirmar navegacion funcional de rutas privadas y estado activo de menu.

Expected:
- La integracion visual no modifica reglas de acceso.
- Login sin sesion sigue redirigiendo correctamente.

## Scenario 2: Dashboard (P2)

1. Revisar mapeo de datos existentes a componentes visuales del UI Kit.
2. Validar que estados loading/empty/error se mantienen con feedback accionable.

Expected:
- Sin cambios de API ni transformaciones de negocio.
- Presentacion consistente con layout autenticado.

## Scenario 3: Trading (P3)

1. Revisar estado de envio y resultado del flujo de trading en UI Kit.
2. Confirmar preservacion de reglas de backend para validacion de planes y ejecucion.

Expected:
- Frontend no decide limites de plan.
- Error/retry mantiene contexto del formulario.

## Scenario 4: Regression Gate

1. Validar checkpoints de auth, private routing, dashboard y trading.
2. Confirmar estrategia de pruebas para `/speckit.tasks` (unit + integration + smoke e2e).

Expected:
- No regresiones funcionales en flujos existentes.
- Lista de tareas implementable sin clarificaciones abiertas.

## Readiness Evidence for /speckit.tasks

- Decisiones de integracion visual y no funcional en `research.md`.
- Entidades/estados de presentacion y checkpoints en `data-model.md`.
- Contrato de responsabilidades frontend-backend/UI en `contracts/frontend-ui-kit-integration.md`.
- Riesgos y mitigaciones documentados en `plan.md`.

## Go/No-Go Checklist (Sprint 012)

- [x] Alcance cerrado confirmado (layout autenticado + Dashboard + Trading).
- [x] Sin cambios backend ni expansion de contratos API.
- [x] Estrategia de regresion definida para auth/routing/trading.
- [x] Estados UX y responsive/accesibilidad incluidos como criterios.
- [x] Revalidacion de governance de stack web para Sprint 012 registrada y aprobada formalmente.

## Closed Scope Checklist (Implementation Gate)

- [x] Solo se implementan cambios en `frontend/` para layout autenticado, Dashboard y Trading.
- [x] No se agregan endpoints ni se modifican payloads backend.
- [x] Notifications y AI Agent se mantienen fuera del rediseno visual completo.
- [x] Se mantiene redireccion a login para usuarios no autenticados.
- [x] Se preserva submit de trading con backend como autoridad de validacion.

## Final Readiness Checklist (/speckit.implement)

- [x] Governance gate aprobado y documentado en `docs/methodology/constitution-exceptions.md`.
- [x] Matriz FR/SC trazada a pruebas y evidencia QA en `docs/qa/cryptocurrency-ui-kit.md`.
- [x] Cobertura de pruebas definida para unit + integration + e2e smoke.
- [x] Validacion contract-freeze backend incluida en evidencia de QA.
