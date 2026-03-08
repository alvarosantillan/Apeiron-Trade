# Tasks: TRDIA - Subscriptions and Payments

**Input**: Design docs from `/specs/004-subscriptions/`  
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/subscriptions.openapi.yaml`

**Tests**: TDD mandatory.

## Phase 1: Setup

- [ ] T001 Create subscriptions module in `backend/src/services/subscriptions/`
- [ ] T002 [P] Create payments module in `backend/src/services/payments/`
- [ ] T003 [P] Create subscription test structure in `backend/tests/*/subscriptions/`

## Phase 2: Foundational

- [ ] T004 Implement MercadoPago client wrapper in `backend/src/services/payments/mercadopago_client.py`
- [ ] T005 [P] Implement webhook signature validator in `backend/src/services/payments/webhook_validator.py`
- [ ] T006 [P] Implement idempotent event processing store in `backend/src/services/payments/event_idempotency.py`
- [ ] T007 Implement plan catalog bootstrap service in `backend/src/services/subscriptions/plan_bootstrap.py`

## Phase 3: US1 - Checkout and Plan Activation (P1)

### Tests

- [ ] T008 [P] [US1] Contract test checkout endpoint in `backend/tests/contract/subscriptions/test_checkout_contract.py`
- [ ] T009 [P] [US1] Integration test approved payment activates plan in `backend/tests/integration/subscriptions/test_plan_activation.py`

### Implementation

- [ ] T010 [US1] Implement create-checkout endpoint in `backend/src/api/subscriptions/checkout.py`
- [ ] T011 [US1] Implement subscription status endpoint in `backend/src/api/subscriptions/status.py`

## Phase 4: US2 - Webhook Processing and Idempotency (P2)

### Tests

- [ ] T012 [P] [US2] Contract test webhook endpoint in `backend/tests/contract/subscriptions/test_webhook_contract.py`
- [ ] T013 [P] [US2] Integration test duplicate webhook handling in `backend/tests/integration/subscriptions/test_webhook_dedup.py`

### Implementation

- [ ] T014 [US2] Implement MercadoPago webhook endpoint in `backend/src/api/subscriptions/webhook.py`
- [ ] T015 [US2] Implement payment-event to subscription-state mapper in `backend/src/services/subscriptions/state_mapper.py`

## Phase 5: US3 - Plan Transitions (P3)

### Tests

- [ ] T016 [P] [US3] Integration test upgrade flow in `backend/tests/integration/subscriptions/test_upgrade.py`
- [ ] T017 [P] [US3] Integration test cancellation at period end in `backend/tests/integration/subscriptions/test_cancellation.py`

### Implementation

- [ ] T018 [US3] Implement upgrade/downgrade service in `backend/src/services/subscriptions/transition_service.py`
- [ ] T019 [US3] Implement cancellation endpoint in `backend/src/api/subscriptions/cancel.py`

## Phase 6: Polish

- [ ] T020 Validate quickstart sandbox scenarios in `specs/004-subscriptions/quickstart.md`
- [ ] T021 Run full subscription test report in `docs/qa/subscriptions.md`
