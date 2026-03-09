from sqlalchemy.exc import OperationalError, SQLAlchemyError

from services.audit.persistence_audit import _redact_dict
from services.persistence.errors import map_db_error


def test_map_operational_error_to_unavailable():
    err = OperationalError("SELECT 1", {}, Exception("down"))
    mapped = map_db_error(err)

    assert mapped.code == "DB_UNAVAILABLE"


def test_map_generic_sqlalchemy_error_to_transaction_error():
    mapped = map_db_error(SQLAlchemyError("bad tx"))

    assert mapped.code == "DB_TRANSACTION_ERROR"


def test_audit_redacts_sensitive_fields():
    payload = {
        "password": "abc",
        "apiKey": "secret-key",
        "refreshToken": "token",
        "safe": "ok",
    }

    redacted = _redact_dict(payload)

    assert redacted["password"] == "***"
    assert redacted["apiKey"] == "***"
    assert redacted["refreshToken"] == "***"
    assert redacted["safe"] == "ok"
