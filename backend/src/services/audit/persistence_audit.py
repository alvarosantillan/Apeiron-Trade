from __future__ import annotations

from uuid import uuid4

from services.persistence.database import session_scope
from services.persistence.models.base import PersistenceAuditEventModel, now_utc

REDACTED_KEYS = {"password", "password_hash", "apiKey", "refreshToken", "token", "secret", "secret_key"}


def _redact_dict(data: dict) -> dict:
    sanitized: dict = {}
    for key, value in data.items():
        if key in REDACTED_KEYS:
            sanitized[key] = "***"
            continue
        sanitized[key] = value
    return sanitized


class PersistenceAuditLogger:
    def log(self, domain: str, action: str, outcome: str, metadata: dict | None = None) -> None:
        payload = _redact_dict(metadata or {})
        with session_scope() as session:
            session.add(
                PersistenceAuditEventModel(
                    id=str(uuid4()),
                    domain=domain,
                    action=action,
                    outcome=outcome,
                    metadata_json=payload,
                    created_at=now_utc(),
                )
            )


persistence_audit = PersistenceAuditLogger()
