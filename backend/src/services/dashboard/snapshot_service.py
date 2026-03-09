from datetime import datetime, timezone

from services.ai_agent.config_store import ai_agent_config_store
from services.execution.execute_order_service import balance_store
from services.subscriptions.plan_bootstrap import plan_bootstrap_service
from services.subscriptions.store import subscription_store
from services.validation.plan_limit_validator import plan_limit_validator


def build_dashboard_snapshot(user_id: str) -> dict:
    subscription = subscription_store.get_status(user_id)
    plan_code = subscription["planCode"]

    ai_cfg = ai_agent_config_store.get(user_id)
    if ai_cfg and ai_cfg.get("isActive", True):
        bot_status = "ACTIVE"
    elif ai_cfg:
        bot_status = "PAUSED"
    else:
        bot_status = "INACTIVE"

    return {
        "planCode": plan_code,
        "operationsUsed": plan_limit_validator.get_used_operations(user_id),
        "operationsLimit": plan_bootstrap_service.get_weekly_limit(plan_code),
        "botStatus": bot_status,
        "balanceSnapshot": balance_store.get_balance(user_id),
        "updatedAt": datetime.now(timezone.utc),
    }
