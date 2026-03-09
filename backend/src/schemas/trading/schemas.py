from datetime import datetime

from pydantic import BaseModel, Field


class BinanceCredentialsRequest(BaseModel):
    api_key: str
    secret_key: str


class BinanceCredentialsStatusResponse(BaseModel):
    active: bool
    api_key_suffix: str | None = None
    verified_at: datetime | None = None


class TradeExecutionRequest(BaseModel):
    request_id: str
    symbol: str
    side: str
    order_type: str
    quantity: float = Field(gt=0)
    limit_price: float | None = None
    is_simulation: bool
    source: str = "manual"


class TradeExecutionResponse(BaseModel):
    request_id: str
    status: str
    execution_type: str
    symbol: str
    side: str
    quantity: float
    message: str


class TradeHistoryItem(BaseModel):
    request_id: str
    status: str
    execution_type: str
    symbol: str
    side: str
    quantity: float
    message: str


class TradeHistoryResponse(BaseModel):
    items: list[TradeHistoryItem]
    page: int
    page_size: int
    total: int
