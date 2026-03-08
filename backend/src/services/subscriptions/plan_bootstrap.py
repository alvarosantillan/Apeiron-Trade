class PlanBootstrapService:
    def __init__(self) -> None:
        self._plans = {
            "free": {"price": 0, "weeklyLimit": 1},
            "plus": {"price": 20, "weeklyLimit": 10},
            "premium": {"price": 200, "weeklyLimit": None},
        }

    def list_plan_codes(self) -> list[str]:
        return list(self._plans.keys())


plan_bootstrap_service = PlanBootstrapService()
