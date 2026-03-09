from services.validation.plan_limit_validator import plan_limit_validator


class WeeklyCounterService:
    def increment_real(self, user_id: str, plan_code: str) -> None:
        plan_limit_validator.register_real_execution(user_id, plan_code)


weekly_counter_service = WeeklyCounterService()
