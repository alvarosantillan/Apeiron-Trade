from datetime import datetime, timezone

from services.execution.execution_repository import execution_repository


def compute_kpis(user_id: str, window: str) -> dict:
    if window not in {"7d", "30d"}:
        raise ValueError("invalid_window")

    executions = execution_repository.get_all_executions(user_id)
    executed = [x for x in executions if x["status"] == "EXECUTED"]
    total = len(executed)

    # Simplified KPI model for in-memory baseline.
    wins = len([x for x in executed if (x.get("executedPrice") or 0) > 0])
    win_rate = (wins / total) if total > 0 else 0.0
    net_pnl = float(total) * 0.5
    avg_return = (net_pnl / total) if total > 0 else 0.0

    return {
        "window": window,
        "totalTrades": total,
        "winRate": win_rate,
        "netPnl": net_pnl,
        "avgReturn": avg_return,
        "updatedAt": datetime.now(timezone.utc),
    }
