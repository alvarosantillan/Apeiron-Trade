from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.exc import OperationalError, SQLAlchemyError


class PersistenceError(RuntimeError):
    code = "DB_TRANSACTION_ERROR"


class PersistenceUnavailableError(PersistenceError):
    code = "DB_UNAVAILABLE"


@dataclass
class ErrorMappingResult:
    code: str
    message: str


def map_db_error(error: Exception) -> ErrorMappingResult:
    if isinstance(error, OperationalError):
        return ErrorMappingResult(code=PersistenceUnavailableError.code, message="Persistence backend is unavailable")
    if isinstance(error, SQLAlchemyError):
        return ErrorMappingResult(code=PersistenceError.code, message="Persistence transaction failed")
    return ErrorMappingResult(code=PersistenceError.code, message="Unexpected persistence error")
