# Tasks: TRDIA - AI Agent

**Input**: Design docs from `/specs/005-ai-agent/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/ai-agent.openapi.yaml`

**Tests**: TDD mandatory.

## Phase 1: Setup

- [x] T001 Create AI agent module in `backend/src/services/ai_agent/`
- [x] T002 [P] Create provider adapters folder in `backend/src/services/ai_providers/`
- [x] T003 [P] Create AI agent test folders in `backend/tests/*/ai_agent/`

## Phase 2: Foundational

- [x] T004 Implement provider adapter interface in `backend/src/services/ai_providers/base_adapter.py`
- [x] T005 [P] Implement decision schema validator in `backend/src/services/ai_agent/decision_validator.py`
- [x] T006 [P] Implement fallback-to-hold policy service in `backend/src/services/ai_agent/fallback_policy.py`
- [x] T007 Implement strategy prompt builder in `backend/src/services/ai_agent/prompt_builder.py`

## Phase 3: US1 - Configure Agent and Provider (P1)

### Tests

- [x] T008 [P] [US1] Contract test config upsert endpoint in `backend/tests/contract/ai_agent/test_config_contract.py`
- [x] T009 [P] [US1] Integration test provider credential validation in `backend/tests/integration/ai_agent/test_config_validation.py`

### Implementation

- [x] T010 [US1] Implement `PUT /v1/ai-agent/config` in `backend/src/api/ai_agent/config.py`
- [x] T011 [US1] Implement config retrieval endpoint in `backend/src/api/ai_agent/config_get.py`

## Phase 4: US2 - Generate and Persist Decisions (P2)

### Tests

- [x] T012 [P] [US2] Integration test valid decision generation in `backend/tests/integration/ai_agent/test_decision_success.py`
- [x] T013 [P] [US2] Integration test fallback on provider failure in `backend/tests/integration/ai_agent/test_decision_fallback.py`

### Implementation

- [x] T014 [US2] Implement decision orchestration service in `backend/src/services/ai_agent/decision_service.py`
- [x] T015 [US2] Implement decision persistence repository in `backend/src/services/ai_agent/decision_repository.py`

## Phase 5: US3 - Plan-aware Manual/Automatic Modes (P3)

### Tests

- [x] T016 [P] [US3] Unit test mode eligibility by plan in `backend/tests/unit/ai_agent/test_mode_policy.py`
- [x] T017 [P] [US3] Integration test free user blocked from automatic mode in `backend/tests/integration/ai_agent/test_free_mode_restriction.py`

### Implementation

- [x] T018 [US3] Implement mode policy validator in `backend/src/services/validation/ai_mode_policy.py`
- [x] T019 [US3] Integrate policy in decision pipeline in `backend/src/services/ai_agent/decision_service.py`

## Phase 6: Polish

- [x] T020 Validate quickstart scenarios in `specs/005-ai-agent/quickstart.md`
- [x] T021 Run AI-agent test baseline in `docs/qa/ai-agent.md`
