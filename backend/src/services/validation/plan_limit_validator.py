from datetime import datetime, timedelta, timezone

from services.subscriptions.plan_bootstrap import plan_bootstrap_service


class PlanLimitValidator:
    def __init__(self) -> None:
        self._weekly_usage: dict[tuple[str, datetime], int] = {}

    def _week_start_utc(self, now: datetime | None = None) -> datetime:
        reference = now or datetime.now(timezone.utc)
        midnight = datetime(reference.year, reference.month, reference.day, tzinfo=timezone.utc)
        return midnight - timedelta(days=reference.weekday())

    def can_execute_real(self, user_id: str, plan_code: str) -> bool:
        limit = plan_bootstrap_service.get_weekly_limit(plan_code)
        if limit is None:
            return True

        key = (user_id, self._week_start_utc())
        current = self._weekly_usage.get(key, 0)
        return current < limit

    def register_real_execution(self, user_id: str, plan_code: str) -> None:
        limit = plan_bootstrap_service.get_weekly_limit(plan_code)
        if limit is None:
            return

        key = (user_id, self._week_start_utc())
        self._weekly_usage[key] = self._weekly_usage.get(key, 0) + 1

    def get_used_operations(self, user_id: str) -> int:
        key = (user_id, self._week_start_utc())
        return self._weekly_usage.get(key, 0)


plan_limit_validator = PlanLimitValidator()
