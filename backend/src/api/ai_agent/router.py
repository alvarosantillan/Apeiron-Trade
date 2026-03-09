from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.middleware.auth_middleware import get_current_user
from schemas.ai_agent.schemas import (
    ConfigResponse,
    DecisionGenerateRequest,
    DecisionListResponse,
    UpsertConfigRequest,
)
from services.ai_agent.config_store import ai_agent_config_store
from services.ai_agent.decision_service import generate_decision_for_user
from services.ai_providers.provider_registry import get_provider_adapter
from services.subscriptions.store import subscription_store
from services.validation.ai_mode_policy import ai_mode_policy_validator

router = APIRouter(prefix="/v1/ai-agent", tags=["ai-agent"])


@router.get("/providers")
def list_providers() -> dict:
    providers = [
        {"code": "OPENAI", "name": "OpenAI"},
        {"code": "GROQ", "name": "Groq"},
        {"code": "DEEPSEEK", "name": "DeepSeek"},
        {"code": "GEMINI", "name": "Gemini"},
    ]
    return {"providers": providers}


@router.get("/strategies")
def list_strategies() -> dict:
    return {
        "strategies": [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "code": "TREND_FOLLOW",
                "name": "Trend Follow",
                "description": "Trend continuation strategy",
                "enabled": True,
            },
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "code": "MEAN_REVERT",
                "name": "Mean Revert",
                "description": "Mean reversion strategy",
                "enabled": True,
            },
        ]
    }


@router.put("/config", response_model=ConfigResponse)
def upsert_config(payload: UpsertConfigRequest, user: dict = Depends(get_current_user)) -> ConfigResponse:
    user_id = user["id"]
    plan_code = subscription_store.get_status(user_id)["planCode"]

    try:
        ai_mode_policy_validator.validate(plan_code, payload.mode)
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="plan restriction")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid mode")

    try:
        adapter = get_provider_adapter(payload.provider)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="unsupported provider")

    if not adapter.validate_credentials(payload.apiKey):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid provider credentials")

    stored = ai_agent_config_store.upsert(user_id, payload.model_dump())
    response_data = {k: v for k, v in stored.items() if k != "apiKey"}
    return ConfigResponse(**response_data)


@router.get("/config", response_model=ConfigResponse)
def get_config(user: dict = Depends(get_current_user)) -> ConfigResponse:
    stored = ai_agent_config_store.get(user["id"])
    if not stored:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="config not found")
    response_data = {k: v for k, v in stored.items() if k != "apiKey"}
    return ConfigResponse(**response_data)


@router.post("/decisions/generate")
def generate_decision(payload: DecisionGenerateRequest, user: dict = Depends(get_current_user)) -> dict:
    try:
        decision = generate_decision_for_user(user["id"], payload.symbol, payload.timeframe)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="missing active config")
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="plan restriction")
    return decision


@router.get("/decisions", response_model=DecisionListResponse)
def list_decisions(user: dict = Depends(get_current_user), limit: int = Query(default=20, ge=1, le=100)) -> DecisionListResponse:
    from services.ai_agent.decision_repository import ai_decision_repository

    return DecisionListResponse(items=ai_decision_repository.list(user["id"], limit=limit))


@router.post("/decisions/{decision_id}/approve")
def approve_decision(decision_id: str, user: dict = Depends(get_current_user)) -> dict:
    return {"decisionId": decision_id, "status": "approved"}


@router.post("/decisions/{decision_id}/reject")
def reject_decision(decision_id: str, user: dict = Depends(get_current_user)) -> dict:
    return {"decisionId": decision_id, "status": "rejected"}
