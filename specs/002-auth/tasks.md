# Tasks: TRDIA - Auth and User Access

**Input**: Design docs from `/specs/002-auth/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/auth.openapi.yaml`

**Tests**: Mandatory by constitution (TDD first, RED -> GREEN -> REFACTOR).

## Phase 1: Setup

- [ ] T001 Create auth module structure in `backend/src/api/auth/` and `backend/src/services/auth/`
- [ ] T002 [P] Create auth schemas in `backend/src/schemas/auth/`
- [ ] T003 [P] Create auth test folders in `backend/tests/{contract,integration,unit}/auth/`

## Phase 2: Foundational

- [ ] T004 Implement password hashing and verification service in `backend/src/services/auth/password_service.py`
- [ ] T005 [P] Implement JWT access/refresh token service in `backend/src/services/auth/token_service.py`
- [ ] T006 [P] Implement auth middleware and user context in `backend/src/api/middleware/auth_middleware.py`
- [ ] T007 Implement auth audit events in `backend/src/services/audit/auth_audit.py`

## Phase 3: US1 - Email Registration/Login (P1)

### Tests (TDD first)

- [ ] T008 [P] [US1] Contract test register endpoint in `backend/tests/contract/auth/test_register_contract.py`
- [ ] T009 [P] [US1] Contract test login endpoint in `backend/tests/contract/auth/test_login_contract.py`
- [ ] T010 [P] [US1] Integration test register-login flow in `backend/tests/integration/auth/test_email_flow.py`

### Implementation

- [ ] T011 [US1] Implement register endpoint in `backend/src/api/auth/register.py`
- [ ] T012 [US1] Implement login endpoint in `backend/src/api/auth/login.py`
- [ ] T013 [US1] Implement refresh endpoint in `backend/src/api/auth/refresh.py`

## Phase 4: US2 - OAuth Login (P2)

### Tests

- [ ] T014 [P] [US2] Contract test OAuth callback in `backend/tests/contract/auth/test_oauth_contract.py`
- [ ] T015 [P] [US2] Integration test Google OAuth flow in `backend/tests/integration/auth/test_google_oauth.py`

### Implementation

- [ ] T016 [US2] Implement Google OAuth handler in `backend/src/api/auth/oauth_google.py`
- [ ] T017 [US2] Implement Facebook OAuth handler in `backend/src/api/auth/oauth_facebook.py`
- [ ] T018 [US2] Map OAuth users to internal profile in `backend/src/services/auth/oauth_user_service.py`

## Phase 5: US3 - Session and Security Controls (P3)

### Tests

- [ ] T019 [P] [US3] Unit test token expiration rules in `backend/tests/unit/auth/test_token_rules.py`
- [ ] T020 [P] [US3] Integration test multi-session behavior in `backend/tests/integration/auth/test_multi_session.py`

### Implementation

- [ ] T021 [US3] Implement session tracking in `backend/src/services/auth/session_service.py`
- [ ] T022 [US3] Implement logout/revoke endpoint in `backend/src/api/auth/logout.py`
- [ ] T023 [US3] Add brute-force protection hooks in `backend/src/services/auth/login_protection.py`

## Phase 6: Polish

- [ ] T024 Update quickstart validation notes in `specs/002-auth/quickstart.md`
- [ ] T025 Run auth test suite and publish report in `docs/qa/auth-baseline.md`
