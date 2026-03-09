from services.validation.plan_limit_validator import plan_limit_validator


def test_free_plan_allows_only_one_real_operation_per_week():
    user_id = "user-weekly-1"

    assert plan_limit_validator.can_execute_real(user_id, "free") is True
    plan_limit_validator.register_real_execution(user_id, "free")

    assert plan_limit_validator.can_execute_real(user_id, "free") is False


def test_premium_plan_has_unlimited_real_operations():
    user_id = "user-weekly-2"

    assert plan_limit_validator.can_execute_real(user_id, "premium") is True
    plan_limit_validator.register_real_execution(user_id, "premium")
    plan_limit_validator.register_real_execution(user_id, "premium")

    assert plan_limit_validator.can_execute_real(user_id, "premium") is True
