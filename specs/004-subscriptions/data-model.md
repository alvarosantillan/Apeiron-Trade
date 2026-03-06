# Data Model - 004-subscriptions

## PlanCatalog

- id: UUID (PK)
- plan_code: enum(free, plus, premium)
- display_name: string
- weekly_limit: integer
- monthly_price: decimal
- currency: string
- provider_plan_id: string (nullable for free)
- is_active: boolean
- created_at: datetime
- updated_at: datetime

Constraints:
- Unique(plan_code)
- Unique(provider_plan_id) where not null

## Subscription

- id: UUID (PK)
- user_id: UUID (FK User)
- plan_code: enum(free, plus, premium)
- status: enum(active, pending, past_due, cancelled)
- provider_subscription_id: string (nullable)
- current_period_start: datetime
- current_period_end: datetime
- next_billing_date: datetime (nullable)
- cancel_at_period_end: boolean
- created_at: datetime
- updated_at: datetime

Constraints:
- Index(user_id, status)

## PaymentRecord

- id: UUID (PK)
- user_id: UUID (FK User)
- subscription_id: UUID (FK Subscription)
- provider_payment_id: string
- amount: decimal
- currency: string
- status: enum(approved, rejected, pending, refunded)
- paid_at: datetime (nullable)
- raw_event_id: string
- created_at: datetime

Constraints:
- Unique(provider_payment_id)
- Index(status, created_at)

## WebhookEvent

- id: UUID (PK)
- provider_event_id: string
- event_type: string
- signature_valid: boolean
- processing_status: enum(received, processed, rejected, duplicate)
- payload_hash: string
- received_at: datetime
- processed_at: datetime (nullable)

Constraints:
- Unique(provider_event_id)
- signature_valid must be true to transition to processed

## SubscriptionAuditLog

- id: UUID (PK)
- user_id: UUID (FK User, nullable)
- subscription_id: UUID (FK Subscription, nullable)
- action: string
- result: enum(success, failure)
- details: jsonb
- created_at: datetime

Constraints:
- details sanitized (no secrets)
