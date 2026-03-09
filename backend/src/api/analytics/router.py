from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.middleware.auth_middleware import get_current_user
from schemas.dashboard.schemas import DashboardKpiResponse, DashboardSummaryResponse
from schemas.history.schemas import TradeDetailResponse, TradeHistoryResponse
from services.audit.trade_detail_audit import trade_detail_audit_store
from services.dashboard.snapshot_service import build_dashboard_snapshot
from services.history.history_query_service import get_trade_detail, list_history
from services.kpi.kpi_service import compute_kpis

router = APIRouter(prefix="/v1", tags=["analytics"])


@router.get("/dashboard/summary", response_model=DashboardSummaryResponse)
def dashboard_summary(user: dict = Depends(get_current_user)) -> DashboardSummaryResponse:
    return DashboardSummaryResponse(**build_dashboard_snapshot(user["id"]))


@router.get("/dashboard/kpis", response_model=DashboardKpiResponse)
def dashboard_kpis(window: str = Query(...), user: dict = Depends(get_current_user)) -> DashboardKpiResponse:
    try:
        return DashboardKpiResponse(**compute_kpis(user["id"], window))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid window")


@router.get("/history/trades", response_model=TradeHistoryResponse)
def history_trades(
    user: dict = Depends(get_current_user),
    from_ts: str | None = Query(default=None, alias="from"),
    to_ts: str | None = Query(default=None, alias="to"),
    status_filter: str | None = Query(default=None, alias="status"),
    is_simulation: bool | None = Query(default=None, alias="isSimulation"),
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = None,
) -> TradeHistoryResponse:
    try:
        payload = list_history(user["id"], from_ts, to_ts, status_filter, is_simulation, limit, cursor)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid filters")
    return TradeHistoryResponse(**payload)


@router.get("/history/trades/{trade_id}", response_model=TradeDetailResponse)
def history_trade_detail(trade_id: str, user: dict = Depends(get_current_user)) -> TradeDetailResponse:
    detail = get_trade_detail(user["id"], trade_id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="trade not found")
    trade_detail_audit_store.log(user["id"], trade_id)
    return TradeDetailResponse(**detail)
