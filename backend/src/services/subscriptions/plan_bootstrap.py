class PlanBootstrapService:
    def __init__(self) -> None:
        self._plans = {
            "free": {"price": 0, "weeklyLimit": 1},
            "plus": {"price": 20, "weeklyLimit": 10},
            "premium": {"price": 200, "weeklyLimit": None},
        }

    def list_plan_codes(self) -> list[str]:
        return list(self._plans.keys())

    def get_weekly_limit(self, plan_code: str) -> int | None:
        return self._plans.get(plan_code, self._plans["free"])["weeklyLimit"]


plan_bootstrap_service = PlanBootstrapService()
