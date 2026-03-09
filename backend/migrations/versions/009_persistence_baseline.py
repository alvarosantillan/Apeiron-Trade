"""Persistence baseline tables for sprint 009.

Revision ID: 009_persistence_baseline
"""

from alembic import op
import sqlalchemy as sa


revision = "009_persistence_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_accounts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=320), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("user_accounts.id"), nullable=False),
        sa.Column("refresh_token", sa.String(length=1024), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_auth_sessions_user_refresh", "auth_sessions", ["user_id", "refresh_token"], unique=True)

    op.create_table(
        "trading_executions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("user_accounts.id"), nullable=False),
        sa.Column("request_id", sa.String(length=128), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_trading_executions_user_request", "trading_executions", ["user_id", "request_id"], unique=True)

    op.create_table(
        "notification_deliveries",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("user_accounts.id"), nullable=False),
        sa.Column("event_id", sa.String(length=128), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_notification_deliveries_user_event", "notification_deliveries", ["user_id", "event_id"])

    op.create_table(
        "ai_agent_configs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("user_accounts.id"), nullable=False, unique=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "persistence_audit_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("domain", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("outcome", sa.String(length=16), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("persistence_audit_events")
    op.drop_table("ai_agent_configs")
    op.drop_index("ix_notification_deliveries_user_event", table_name="notification_deliveries")
    op.drop_table("notification_deliveries")
    op.drop_index("ix_trading_executions_user_request", table_name="trading_executions")
    op.drop_table("trading_executions")
    op.drop_index("ix_auth_sessions_user_refresh", table_name="auth_sessions")
    op.drop_table("auth_sessions")
    op.drop_table("user_accounts")
