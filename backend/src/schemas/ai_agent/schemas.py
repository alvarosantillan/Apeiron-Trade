from datetime import datetime

from pydantic import BaseModel, Field


class UpsertConfigRequest(BaseModel):
    provider: str
    apiKey: str = Field(min_length=10)
    strategyId: str
    riskProfile: str
    mode: str
    isActive: bool = True


class ConfigResponse(BaseModel):
    id: str
    provider: str
    strategyId: str
    riskProfile: str
    mode: str
    isActive: bool
    updatedAt: datetime


class DecisionGenerateRequest(BaseModel):
    symbol: str
    timeframe: str


class Decision(BaseModel):
    id: str
    action: str
    confidence: float
    riskLevel: str
    status: str
    symbol: str
    timeframe: str
    reasoning: str
    fallbackReason: str | None = None
    decisionTs: datetime


class DecisionListResponse(BaseModel):
    items: list[Decision]
