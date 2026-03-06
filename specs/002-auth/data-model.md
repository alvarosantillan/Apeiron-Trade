# Data Model - 002-auth

## User

- id: UUID (PK)
- email: string (unique, normalized)
- password_hash: string (nullable for OAuth-only users)
- auth_provider: enum(email, google, facebook)
- provider_user_id: string (nullable, indexed)
- plan: enum(free, plus, premium)
- status: enum(active, blocked, deleted)
- created_at: datetime
- updated_at: datetime

Constraints:
- Unique(email)
- Unique(auth_provider, provider_user_id) when provider_user_id is not null

## RefreshSession

- id: UUID (PK)
- user_id: UUID (FK User)
- refresh_token_hash: string
- device_info: string
- ip_address: string
- expires_at: datetime
- revoked_at: datetime (nullable)
- rotated_from_id: UUID (nullable)
- created_at: datetime

Constraints:
- Index(user_id, revoked_at)
- Token hash never stored in plain text

## AuthAuditLog

- id: UUID (PK)
- user_id: UUID (nullable FK User)
- event_type: enum(register_attempt, register_success, login_success, login_failed, oauth_login_success, refresh_success, refresh_failed, logout_success, revoke_all_sessions)
- result: enum(success, failure)
- ip_address: string
- user_agent: string
- metadata: jsonb
- created_at: datetime

Constraints:
- created_at indexed
- metadata must not contain secrets


