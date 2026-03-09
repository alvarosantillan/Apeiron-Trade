class AIModePolicyValidator:
    def validate(self, plan_code: str, mode: str) -> None:
        if mode not in {"MANUAL", "AUTOMATIC"}:
            raise ValueError("invalid_mode")
        if plan_code == "free" and mode == "AUTOMATIC":
            raise PermissionError("free_plan_automatic_not_allowed")


ai_mode_policy_validator = AIModePolicyValidator()
