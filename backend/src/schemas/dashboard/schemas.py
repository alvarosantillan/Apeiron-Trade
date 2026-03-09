from datetime import datetime

from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    planCode: str
    operationsUsed: int
    operationsLimit: int | None = None
    botStatus: str
    balanceSnapshot: float | None = None
    updatedAt: datetime


class DashboardKpiResponse(BaseModel):
    window: str
    totalTrades: int
    winRate: float
    netPnl: float
    avgReturn: float
    updatedAt: datetime
