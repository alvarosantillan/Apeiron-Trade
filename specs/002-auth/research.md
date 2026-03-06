# Research - 002-auth

## Decision 1: Session Model

- Decision: Use short-lived access token + rotating refresh token.
- Rationale: Limits impact of access token leakage and blocks replay when refresh is rotated.
- Alternatives considered:
  - Long-lived JWT only: rejected due to high compromise window.
  - Server session only: rejected for mobile scalability and stateless API goal.

## Decision 2: OAuth Identity Mapping

- Decision: Store provider identity (`provider`, `provider_user_id`) and map to one internal user.
- Rationale: Prevents duplicate users and keeps deterministic login behavior.
- Alternatives considered:
  - Email-only matching: rejected because providers may return unverified or changed emails.

## Decision 3: Auth Rate Limiting

- Decision: Apply rate limit by IP + account target on register/login/refresh.
- Rationale: Better brute-force protection than single-dimensional limit.
- Alternatives considered:
  - IP-only rate limit: rejected because NAT/proxy scenarios can hurt legitimate users.

## Decision 4: Audit Granularity

- Decision: Persist security-relevant auth events (attempt/success/failure/refresh/revoke/logout).
- Rationale: Required for incident response and compliance with constitution.
- Alternatives considered:
  - Log-only observability: rejected due to weaker queryability and retention control.


