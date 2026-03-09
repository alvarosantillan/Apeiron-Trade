from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.middleware.auth_middleware import get_current_user
from schemas.trading.schemas import (
    BinanceCredentialsRequest,
    BinanceCredentialsStatusResponse,
    TradeHistoryResponse,
    TradeExecutionRequest,
    TradeExecutionResponse,
)
from services.binance.credential_service import credential_store
from services.execution.execute_order_service import ExecutionError, execute_order
from services.execution.execution_repository import execution_repository
from services.execution.idempotency_service import idempotency_service
from services.execution.paper_execution_service import PaperExecutionError, execute_paper_order
from services.subscriptions.store import subscription_store
from services.validation.plan_limit_validator import plan_limit_validator

router = APIRouter(prefix="/v1/trading", tags=["trading"])


@router.post("/binance/credentials", status_code=status.HTTP_200_OK)
def save_binance_credentials(payload: BinanceCredentialsRequest, user: dict = Depends(get_current_user)) -> dict:
    try:
        credential_store.upsert(user["id"], payload.api_key, payload.secret_key)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid credentials")
    return {"status": "verified"}


@router.get("/binance/credentials/status", response_model=BinanceCredentialsStatusResponse)
def get_binance_credential_status(user: dict = Depends(get_current_user)) -> BinanceCredentialsStatusResponse:
    return BinanceCredentialsStatusResponse(**credential_store.status(user["id"]))


@router.post("/execute", response_model=TradeExecutionResponse)
def execute_trade(payload: TradeExecutionRequest, user: dict = Depends(get_current_user)) -> TradeExecutionResponse:
    user_id = user["id"]

    current_subscription = subscription_store.get_status(user_id)
    plan_code = current_subscription["planCode"]

    if not payload.is_simulation and not credential_store.has_active_credentials(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="missing active binance credentials")

    if not payload.is_simulation and not plan_limit_validator.can_execute_real(user_id, plan_code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="weekly_limit_exceeded")

    if not idempotency_service.check_and_mark(user_id, payload.request_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="duplicate request id")

    try:
        if payload.is_simulation:
            result = execute_paper_order(payload.model_dump())
        else:
            result = execute_order(user_id, payload.model_dump())
            if result["status"] == "executed":
                plan_limit_validator.register_real_execution(user_id, plan_code)
    except (ValueError, ExecutionError, PaperExecutionError):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid execution payload")

    return TradeExecutionResponse(**result)


@router.get("/history", response_model=TradeHistoryResponse)
def get_trade_history(
    user: dict = Depends(get_current_user),
    is_simulation: bool | None = None,
    status_filter: str | None = Query(default=None, alias="status"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> TradeHistoryResponse:
    items, total = execution_repository.list(
        is_simulation=is_simulation,
        status=status_filter,
        page=page,
        page_size=page_size,
    )
    return TradeHistoryResponse(items=items, page=page, page_size=page_size, total=total)
