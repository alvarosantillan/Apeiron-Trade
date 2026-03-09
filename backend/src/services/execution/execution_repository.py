class ExecutionRepository:
    def __init__(self) -> None:
        self._executions: list[dict] = []

    def add(self, execution: dict) -> None:
        self._executions.append(execution)

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
