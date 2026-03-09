from datetime import datetime

from pydantic import BaseModel


class TradeHistoryItemResponse(BaseModel):
    tradeId: str
    symbol: str
    side: str
    status: str
    executedPrice: float | None = None
    quantity: float
    isSimulation: bool
    pnl: float | None = None
    createdAt: datetime


class TradeHistoryResponse(BaseModel):
    items: list[TradeHistoryItemResponse]
    nextCursor: str | None = None


class TradeDetailResponse(BaseModel):
    tradeId: str
    requestId: str
    status: str
    symbol: str
    side: str
    quantity: float
    executedPrice: float | None = None
    isSimulation: bool
    failureReason: str | None = None
    executionTrace: dict
    createdAt: datetime
