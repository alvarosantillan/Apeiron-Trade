from services.ai_agent.config_store import ai_agent_config_store
from services.ai_agent.decision_repository import ai_decision_repository
from services.ai_agent.decision_validator import validate_decision_shape
from services.ai_agent.fallback_policy import fallback_hold_decision
from services.ai_agent.prompt_builder import build_strategy_prompt
from services.ai_providers.provider_registry import get_provider_adapter
from services.subscriptions.store import subscription_store
from services.validation.ai_mode_policy import ai_mode_policy_validator


def generate_decision_for_user(user_id: str, symbol: str, timeframe: str) -> dict:
    config = ai_agent_config_store.get(user_id)
    if not config or not config.get("isActive", True):
        raise ValueError("missing_active_config")

    plan_code = subscription_store.get_status(user_id)["planCode"]
    ai_mode_policy_validator.validate(plan_code, config["mode"])

    prompt = build_strategy_prompt(config["strategyId"], config["riskProfile"], symbol, timeframe)

    try:
        adapter = get_provider_adapter(config["provider"])
        raw = adapter.generate_decision(symbol, timeframe, prompt)
        validate_decision_shape(raw)
    except Exception as exc:
        raw = fallback_hold_decision(symbol, timeframe, str(exc))

    if config["mode"] == "AUTOMATIC" and raw["status"] == "PENDING_APPROVAL":
        raw["status"] = "EXECUTED"

    recent_equivalent = ai_decision_repository.find_recent_equivalent(
        user_id,
        symbol=raw["symbol"],
        timeframe=raw["timeframe"],
        action=raw["action"],
    )
    if recent_equivalent:
        return recent_equivalent

    return ai_decision_repository.add(user_id, raw)
