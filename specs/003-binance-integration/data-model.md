# Data Model - 003-binance-integration

## BinanceCredential

- id: UUID (PK)
- user_id: UUID (FK User, unique)
- api_key_encrypted: string
- secret_key_encrypted: string
- masked_key_suffix: string(4)
- is_active: boolean
- last_verified_at: datetime (nullable)
- created_at: datetime
- updated_at: datetime

Constraints:
- Unique(user_id)
- Secrets never stored in plain text

## TradeExecutionRequest

- id: UUID (PK)
- request_id: string (idempotency key, unique per user)
- user_id: UUID (FK User)
- symbol: string
- side: enum(BUY, SELL)
- order_type: enum(MARKET, LIMIT)
- quantity: decimal
- limit_price: decimal (nullable)
- is_simulation: boolean
- source: enum(manual, agent)
- created_at: datetime

Constraints:
- Unique(user_id, request_id)
- quantity > 0
- limit_price required when order_type = LIMIT

## TradeExecution

- id: UUID (PK)
- request_ref_id: UUID (FK TradeExecutionRequest)
- user_id: UUID (FK User)
- symbol: string
- side: enum(BUY, SELL)
- status: enum(executed, failed, blocked, cancelled)
- executed_price: decimal (nullable)
- quantity: decimal
- exchange_order_id: string (nullable)
- is_simulation: boolean
- failure_reason: string (nullable)
- created_at: datetime

Constraints:
- Index(user_id, created_at desc)
- status blocked/failed must include failure_reason

## OperationCounter

- id: UUID (PK)
- user_id: UUID (FK User)
- week_start_utc: datetime
- operations_used: integer
- plan_limit: integer
- last_updated_at: datetime

Constraints:
- Unique(user_id, week_start_utc)
- operations_used >= 0

## TradeAuditLog

- id: UUID (PK)
- trade_execution_id: UUID (FK TradeExecution, nullable)
- user_id: UUID (FK User)
- event_type: string
- result: enum(success, failure)
- details: jsonb
- created_at: datetime

Constraints:
- details cannot contain secrets
