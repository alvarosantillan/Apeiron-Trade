# Implementation Plan: TRDIA - Auth Feature

**Branch**: `002-auth` | **Date**: 2026-03-06 | **Spec**: `specs/002-auth/spec.md`
**Input**: Feature specification from `/specs/002-auth/spec.md`

## Summary

Implementar autenticación segura para TRDIA con tres flujos de acceso (`email/password`, Google OAuth, Facebook OAuth), gestión de sesión con `access + refresh tokens`, endpoints de perfil y auditoría de seguridad. El enfoque usa backend-first validation, diseño modular, y TDD estricto para prevenir regresiones en un módulo crítico.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, python-jose, passlib[bcrypt], authlib (OAuth), redis (opcional para rate-limit)  
**Storage**: PostgreSQL externa (tablas `users`, `refresh_sessions`, `auth_audit_logs`)  
**Testing**: pytest, pytest-asyncio, httpx TestClient, pytest-cov  
**Target Platform**: API backend Linux container + app móvil React Native  
**Project Type**: Mobile + API (backend service)  
**Performance Goals**: login p95 < 1.5s, refresh p95 < 1.0s  
**Constraints**: no exponer secretos en logs; rotación de refresh tokens; rate-limit en auth endpoints  
**Scale/Scope**: MVP inicial 1k usuarios activos, crecimiento progresivo

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Verify compliance with TRDIA Constitution (.specify/memory/constitution.md):**

- [x] **Principle I (Spec-Driven)**: Spec `specs/002-auth/spec.md` completa antes de código
- [x] **Principle II (TDD)**: Plan de tests definido (unit, contract, integration) previo a implementación
- [x] **Principle III (Security-First)**:
  - [x] No credentials in code/logs
  - [x] Input validation defined
  - [x] Password/token hashing strategy documented
  - [x] Audit logging requirements identified
- [x] **Principle IV (Modular)**: Encaja en `backend/src/api`, `backend/src/services`, `backend/src/models`
- [x] **Principle V (Validation-Strict)**:
  - [x] Validación backend definida para auth/session
  - [x] Plan limits no aplican en auth (documentado en spec)
  - [x] No frontend-only validation for business logic
- [x] **Principle VI (Observability)**: Métricas y logging definidos en spec
- [x] **Principle VII (Progressive Enhancement)**: Alcance MVP sin complejidad prematura

## Project Structure

### Documentation (this feature)

```text
specs/002-auth/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── auth.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── auth/
│   ├── services/
│   │   └── auth/
│   ├── models/
│   ├── schemas/
│   └── security/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
└── src/
    └── screens/
        └── auth/
```

**Structure Decision**: Se adopta estructura `Mobile + API`; esta feature se implementa principalmente en `backend/`, con integración mínima de consumo en `frontend/`.

## Phase Plan

### Phase 0 - Research Decisions

1. Estrategia de tokens: JWT corto + refresh rotatorio (hash en DB)
2. Estrategia OAuth: validación de token proveedor y mapeo de identidad por email/provider ID
3. Estrategia de rate-limit: por IP y por cuenta en endpoints sensibles

### Phase 1 - Design Artifacts

1. `data-model.md` con entidades `User`, `RefreshSession`, `AuthAuditLog`
2. `contracts/auth.openapi.yaml` con endpoints de auth y profile
3. `quickstart.md` con flujos de prueba manual para QA

### Phase 2 - Implementation Ready

Resultado esperado para `/speckit.tasks`:
- tasks por historias P1-P4
- tests-first obligatorios
- secuencia: modelos -> servicios -> endpoints -> auditoría -> métricas

## Testing Strategy (TDD Gate)

1. Contract tests para `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`, `/users/me`
2. Integration tests para OAuth login, refresh rotation, revoke all sessions, rate-limit
3. Unit tests para hashing, emisión/validación JWT y validadores de entrada
4. Gate de coverage:
   - módulo auth: >= 90%
   - global backend: >= 80%

## Risks & Mitigations

- Riesgo: replay de refresh token
  - Mitigación: rotación + invalidación de cadena previa
- Riesgo: brute-force en login
  - Mitigación: rate-limit + auditoría + alertas
- Riesgo: inconsistencia cuentas OAuth/email
  - Mitigación: regla de vinculación determinística por provider ID + email verificado

## Complexity Tracking

No constitutional violations detected.


