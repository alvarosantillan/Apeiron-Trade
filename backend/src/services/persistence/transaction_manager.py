from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from sqlalchemy.exc import OperationalError, SQLAlchemyError

from services.audit.persistence_audit import persistence_audit
from services.persistence.errors import PersistenceError, PersistenceUnavailableError

T = TypeVar("T")


def run_transaction(action: str, operation: Callable[[], T]) -> T:
    try:
        result = operation()
        persistence_audit.log(domain="DB", action=action, outcome="SUCCESS")
        return result
    except OperationalError as exc:
        persistence_audit.log(domain="DB", action=action, outcome="FAILURE", metadata={"error": str(exc)})
        raise PersistenceUnavailableError("Persistence backend is unavailable") from exc
    except SQLAlchemyError as exc:
        persistence_audit.log(domain="DB", action=action, outcome="FAILURE", metadata={"error": str(exc)})
        raise PersistenceError("Persistence transaction failed") from exc
