from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select

from services.persistence.database import initialize_database, session_scope
from services.persistence.models.base import (
    AIAgentConfigModel,
    NotificationDeliveryModel,
    TradingExecutionModel,
    UserAccountModel,
)
from services.validation.db_settings import load_db_settings


DEMO_EMAIL = "demo@trdia.local"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _seed_execution(session, user_id: str, sequence: int) -> None:
    request_id = f"seed-order-{sequence:03d}"
    existing_exec = session.execute(
        select(TradingExecutionModel).where(
            TradingExecutionModel.user_id == user_id,
            TradingExecutionModel.request_id == request_id,
        )
    ).scalar_one_or_none()

    if existing_exec is None:
        session.add(
            TradingExecutionModel(
                id=str(uuid4()),
                user_id=user_id,
                request_id=request_id,
                payload={
                    "symbol": "BTCUSDT",
                    "side": "BUY" if sequence % 2 else "SELL",
                    "type": "MARKET",
                    "quantity": f"0.00{(sequence % 9) + 1}",
                    "price": None,
                    "status": "FILLED",
                    "executedAt": now_iso(),
                },
            )
        )
        print(f"Created trading execution: {request_id}")


def _seed_notification(session, user_id: str, sequence: int) -> None:
    event_id = f"seed-notif-{sequence:03d}"
    existing_notif = session.execute(
        select(NotificationDeliveryModel).where(
            NotificationDeliveryModel.user_id == user_id,
            NotificationDeliveryModel.event_id == event_id,
        )
    ).scalar_one_or_none()

    if existing_notif is None:
        session.add(
            NotificationDeliveryModel(
                id=str(uuid4()),
                user_id=user_id,
                event_id=event_id,
                payload={
                    "channel": "push",
                    "title": "Operacion ejecutada",
                    "body": f"Evento demo #{sequence}",
                    "deliveredAt": now_iso(),
                },
            )
        )
        print(f"Created notification delivery: {event_id}")


def seed_demo_data(executions: int) -> None:
    # Align seed target with runtime DB configuration used by the API startup.
    settings = load_db_settings()
    os.environ["DATABASE_URL"] = settings.database_url

    # Ensure tables exist before seeding records.
    initialize_database()

    with session_scope() as session:
        user = session.execute(
            select(UserAccountModel).where(UserAccountModel.email == DEMO_EMAIL)
        ).scalar_one_or_none()

        if user is None:
            user = UserAccountModel(
                id=str(uuid4()),
                email=DEMO_EMAIL,
                password_hash=None,
            )
            session.add(user)
            session.flush()
            print(f"Created user: {user.email} ({user.id})")
        else:
            print(f"User already exists: {user.email} ({user.id})")

        for sequence in range(1, executions + 1):
            _seed_execution(session, user.id, sequence)
            _seed_notification(session, user.id, sequence)

        existing_ai = session.execute(
            select(AIAgentConfigModel).where(AIAgentConfigModel.user_id == user.id)
        ).scalar_one_or_none()

        if existing_ai is None:
            session.add(
                AIAgentConfigModel(
                    id=str(uuid4()),
                    user_id=user.id,
                    payload={
                        "mode": "balanced",
                        "riskProfile": "moderate",
                        "maxDailyOrders": 5,
                        "updatedAt": now_iso(),
                    },
                )
            )
            print("Created AI agent config")
        else:
            existing_ai.payload = {
                "mode": "balanced",
                "riskProfile": "moderate",
                "maxDailyOrders": 5,
                "updatedAt": now_iso(),
            }
            print("Updated AI agent config")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed demo data for local testing")
    parser.add_argument(
        "--executions",
        type=int,
        default=1,
        help="Number of execution/notification demo records to ensure",
    )
    args = parser.parse_args()

    seed_demo_data(max(1, args.executions))
    print("Seed completed")
