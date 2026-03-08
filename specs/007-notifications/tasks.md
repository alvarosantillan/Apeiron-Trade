# Tasks: TRDIA - Notifications and Alerts

**Input**: Design docs from `/specs/007-notifications/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/notifications.openapi.yaml`

**Tests**: TDD mandatory.

## Phase 1: Setup

- [ ] T001 Create notifications module in `backend/src/services/notifications/`
- [ ] T002 [P] Create notification schemas in `backend/src/schemas/notifications/`
- [ ] T003 [P] Create notification tests in `backend/tests/*/notifications/`

## Phase 2: Foundational

- [ ] T004 Implement push provider abstraction in `backend/src/services/notifications/push_provider.py`
- [ ] T005 [P] Implement deduplication service in `backend/src/services/notifications/dedup_service.py`
- [ ] T006 [P] Implement retry policy service in `backend/src/services/notifications/retry_policy.py`
- [ ] T007 Implement token lifecycle manager in `backend/src/services/notifications/token_service.py`

## Phase 3: US1 - Register Devices and Send Trading Alerts (P1)

### Tests

- [ ] T008 [P] [US1] Contract test device token upsert in `backend/tests/contract/notifications/test_device_tokens_contract.py`
- [ ] T009 [P] [US1] Integration test trading event push delivery in `backend/tests/integration/notifications/test_trading_push_delivery.py`

### Implementation

- [ ] T010 [US1] Implement device token endpoints in `backend/src/api/notifications/device_tokens.py`
- [ ] T011 [US1] Implement event-to-delivery pipeline in `backend/src/services/notifications/delivery_service.py`

## Phase 4: US2 - Preferences and Critical Priority (P2)

### Tests

- [ ] T012 [P] [US2] Contract test preferences update in `backend/tests/contract/notifications/test_preferences_contract.py`
- [ ] T013 [P] [US2] Integration test preference filtering in `backend/tests/integration/notifications/test_preference_filtering.py`

### Implementation

- [ ] T014 [US2] Implement preference endpoints in `backend/src/api/notifications/preferences.py`
- [ ] T015 [US2] Implement critical-priority override policy in `backend/src/services/notifications/priority_policy.py`

## Phase 5: US3 - Delivery Tracking and Retries (P3)

### Tests

- [ ] T016 [P] [US3] Integration test transient failure retry in `backend/tests/integration/notifications/test_retry_flow.py`
- [ ] T017 [P] [US3] Integration test invalid token drop in `backend/tests/integration/notifications/test_invalid_token_drop.py`

### Implementation

- [ ] T018 [US3] Implement delivery status transitions in `backend/src/services/notifications/delivery_status_service.py`
- [ ] T019 [US3] Implement history endpoint in `backend/src/api/notifications/history.py`

## Phase 6: Polish

- [ ] T020 Validate quickstart scenarios in `specs/007-notifications/quickstart.md`
- [ ] T021 Run notifications test baseline in `docs/qa/notifications.md`
