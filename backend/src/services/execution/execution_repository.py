class ExecutionRepository:
    def __init__(self) -> None:
        self._executions: list[dict] = []

    def add(self, execution: dict) -> None:
        self._executions.append(execution)


execution_repository = ExecutionRepository()
