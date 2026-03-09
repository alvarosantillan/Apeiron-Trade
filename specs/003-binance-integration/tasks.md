# Tasks: TRDIA - Binance Integration

**Input**: Design docs from `/specs/003-binance-integration/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/trading.openapi.yaml`

**Tests**: TDD mandatory.

## Phase 1: Setup

- [x] T001 Create Binance integration module in `backend/src/services/binance/`
- [x] T002 [P] Create trading schemas in `backend/src/schemas/trading/`
- [x] T003 [P] Create tests structure under `backend/tests/*/trading/`

## Phase 2: Foundational

- [x] T004 Implement credential encryption/decryption adapter in `backend/src/services/binance/credential_service.py`
- [x] T005 [P] Implement exchange client abstraction in `backend/src/services/binance/client.py`
- [x] T006 [P] Implement symbol/precision validator in `backend/src/services/binance/market_rules.py`
- [x] T007 Implement idempotency guard in `backend/src/services/execution/idempotency_service.py`

## Phase 3: US1 - Store and Validate Credentials (P1)

### Tests

- [x] T008 [P] [US1] Contract test credentials endpoint in `backend/tests/contract/trading/test_credentials_contract.py`
- [x] T009 [P] [US1] Integration test credential validation in `backend/tests/integration/trading/test_credentials_validation.py`

### Implementation

- [x] T010 [US1] Implement credentials upsert endpoint in `backend/src/api/trading/credentials.py`
- [x] T011 [US1] Implement active-credentials status endpoint in `backend/src/api/trading/credentials_status.py`

## Phase 4: US2 - Execute Spot Orders (P2)

### Tests

- [x] T012 [P] [US2] Contract test execute endpoint in `backend/tests/contract/trading/test_execution_contract.py`
- [x] T013 [P] [US2] Integration test successful execution in `backend/tests/integration/trading/test_execute_success.py`
- [x] T014 [P] [US2] Integration test insufficient balance in `backend/tests/integration/trading/test_execute_balance_fail.py`

### Implementation

- [x] T015 [US2] Implement execute order service in `backend/src/services/execution/execute_order_service.py`
- [x] T016 [US2] Implement execute endpoint in `backend/src/api/trading/executions.py`
- [x] T017 [US2] Persist execution results in `backend/src/services/execution/execution_repository.py`

## Phase 5: US3 - Paper Trading and Limits (P3)

### Tests

- [x] T018 [P] [US3] Integration test paper execution non-consumption in `backend/tests/integration/trading/test_paper_mode.py`
- [x] T019 [P] [US3] Unit test weekly counter rule in `backend/tests/unit/trading/test_weekly_counter.py`

### Implementation

- [x] T020 [US3] Implement paper execution adapter in `backend/src/services/execution/paper_execution_service.py`
- [x] T021 [US3] Integrate plan-limit validation in `backend/src/services/validation/plan_limit_validator.py`

## Phase 6: Polish

- [x] T022 Run trading integration test suite and baseline report in `docs/qa/binance-integration.md`
- [x] T023 Validate quickstart scenarios in `specs/003-binance-integration/quickstart.md`
