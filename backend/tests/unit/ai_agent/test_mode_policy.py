import pytest

from services.validation.ai_mode_policy import ai_mode_policy_validator


def test_free_plan_manual_allowed():
    ai_mode_policy_validator.validate("free", "MANUAL")


def test_free_plan_automatic_blocked():
    with pytest.raises(PermissionError):
        ai_mode_policy_validator.validate("free", "AUTOMATIC")


def test_plus_plan_automatic_allowed():
    ai_mode_policy_validator.validate("plus", "AUTOMATIC")
