from datetime import datetime, timezone
from uuid import uuid4

from services.persistence.database import session_scope
from services.persistence.json_utils import make_json_safe
from services.persistence.models.base import TradingExecutionModel


class ExecutionRepository:
    def __init__(self) -> None:
        self._executions: list[dict] = []
        self._by_user: dict[str, list[dict]] = {}
        self._by_id: dict[str, dict] = {}

    def add(self, execution: dict) -> None:
        user_id = execution.get("userId") or execution.get("user_id") or ""
        self.add_execution(user_id, execution)

    @staticmethod
    def _request_id(execution: dict) -> str:
        request_id = execution.get("requestId") or execution.get("request_id")
        if not request_id:
            raise KeyError("requestId")
        return request_id

    @staticmethod
    def _as_datetime(value: object, fallback: datetime) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            normalized = value.replace("Z", "+00:00")
            try:
                return datetime.fromisoformat(normalized)
            except ValueError:
                return fallback
        return fallback

    def add_execution(self, user_id: str, execution: dict) -> None:
        now = datetime.now(timezone.utc)
        request_id = self._request_id(execution)
        execution_id = execution.get("id") or str(uuid4())
        created_at_raw = execution.get("createdAt") or execution.get("created_at") or now
        updated_at_raw = execution.get("updatedAt") or execution.get("updated_at") or now
        created_at = self._as_datetime(created_at_raw, now)
        updated_at = self._as_datetime(updated_at_raw, now)
        payload = make_json_safe(execution)

        with session_scope() as session:
            item = (
                session.query(TradingExecutionModel)
                .filter(TradingExecutionModel.user_id == user_id, TradingExecutionModel.request_id == request_id)
                .first()
            )
            if item:
                item.payload = payload
                item.updated_at = updated_at
                return
            session.add(
                TradingExecutionModel(
                    id=execution_id,
                    user_id=user_id,
                    request_id=request_id,
                    payload=payload,
                    created_at=created_at,
                    updated_at=updated_at,
                )
            )

    def get_execution(self, execution_id: str) -> dict | None:
        with session_scope() as session:
            item = session.query(TradingExecutionModel).filter(TradingExecutionModel.id == execution_id).first()
            if not item:
                return None
            return item.payload

    def get_by_request_id(self, user_id: str, request_id: str) -> dict | None:
        with session_scope() as session:
            item = (
                session.query(TradingExecutionModel)
                .filter(TradingExecutionModel.user_id == user_id, TradingExecutionModel.request_id == request_id)
                .first()
            )
            if not item:
                return None
            return item.payload

    def update_execution(self, execution: dict) -> None:
        with session_scope() as session:
            item = session.query(TradingExecutionModel).filter(TradingExecutionModel.id == execution["id"]).first()
            if not item:
                return
            item.payload = make_json_safe(execution)
            updated_at_raw = execution.get("updatedAt") or execution.get("updated_at") or datetime.now(timezone.utc)
            item.updated_at = self._as_datetime(updated_at_raw, datetime.now(timezone.utc))

    def list_executions(
        self,
        user_id: str,
        limit: int = 20,
        status: str | None = None,
        execution_type: str | None = None,
    ) -> list[dict]:
        with session_scope() as session:
            items = [x.payload for x in session.query(TradingExecutionModel).filter(TradingExecutionModel.user_id == user_id).all()]
        if status:
            items = [item for item in items if item["status"] == status]
        if execution_type:
            items = [
                item
                for item in items
                if item.get("executionType") == execution_type or item.get("execution_type") == execution_type
            ]
        items.sort(key=lambda item: item.get("createdAt") or item.get("created_at"), reverse=True)
        return items[:limit]

    def get_all_executions(self, user_id: str) -> list[dict]:
        with session_scope() as session:
            return [x.payload for x in session.query(TradingExecutionModel).filter(TradingExecutionModel.user_id == user_id).all()]

    def list(
        self,
        user_id: str | None = None,
        is_simulation: bool | None = None,
        status: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict], int]:
        with session_scope() as session:
            query = session.query(TradingExecutionModel)
            if user_id:
                query = query.filter(TradingExecutionModel.user_id == user_id)
            filtered = [x.payload for x in query.all()]

        if is_simulation is not None:
            expected = "PAPER" if is_simulation else "REAL"
            filtered = [
                item
                for item in filtered
                if item.get("execution_type") == expected or item.get("executionType") == expected
            ]

        if status:
            filtered = [item for item in filtered if item["status"] == status]

        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end], total


execution_repository = ExecutionRepository()
