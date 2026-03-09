"""Additional indexes for persistence critical paths.

Revision ID: 009_persistence_indexes
"""

from alembic import op


revision = "009_persistence_indexes"
down_revision = "009_persistence_baseline"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_notification_deliveries_user_created", "notification_deliveries", ["user_id", "created_at"])
    op.create_index("ix_trading_executions_user_updated", "trading_executions", ["user_id", "updated_at"])


def downgrade() -> None:
    op.drop_index("ix_trading_executions_user_updated", table_name="trading_executions")
    op.drop_index("ix_notification_deliveries_user_created", table_name="notification_deliveries")
