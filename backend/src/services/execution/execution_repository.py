class ExecutionRepository:
    def __init__(self) -> None:
        self._executions: list[dict] = []
        self._by_user: dict[str, list[dict]] = {}
        self._by_id: dict[str, dict] = {}

    def add(self, execution: dict) -> None:
        self._executions.append(execution)

    def add_execution(self, user_id: str, execution: dict) -> None:
        if user_id not in self._by_user:
            self._by_user[user_id] = []
        self._by_user[user_id].insert(0, execution)
        self._by_id[execution["id"]] = execution

    def get_execution(self, execution_id: str) -> dict | None:
        return self._by_id.get(execution_id)

    def update_execution(self, execution: dict) -> None:
        self._by_id[execution["id"]] = execution

    def list_executions(
        self,
        user_id: str,
        limit: int = 20,
        status: str | None = None,
        execution_type: str | None = None,
    ) -> list[dict]:
        items = self._by_user.get(user_id, [])
        if status:
            items = [item for item in items if item["status"] == status]
        if execution_type:
            items = [item for item in items if item["executionType"] == execution_type]
        return items[:limit]

    def list(
        self,
        is_simulation: bool | None = None,
        status: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict], int]:
        filtered = self._executions

        if is_simulation is not None:
            expected = "PAPER" if is_simulation else "REAL"
            filtered = [item for item in filtered if item["execution_type"] == expected]

        if status:
            filtered = [item for item in filtered if item["status"] == status]

        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end], total


execution_repository = ExecutionRepository()
