from fastapi import FastAPI

from api.auth.router import router as auth_router
from api.ai_agent.router import router as ai_agent_router
from api.analytics.router import router as analytics_router
from api.notifications.router import router as notifications_router
from api.subscriptions.router import router as subscriptions_router
from api.trading.router import router as trading_router
from api.users.router import router as users_router
from api.middleware.persistence_error_handler import install_persistence_error_handler
from services.persistence.database import initialize_database, reset_database_engine
from services.validation.db_settings import load_db_settings


def _bootstrap_persistence() -> None:
	settings = load_db_settings()
	# Keep a single source of truth for database URL used by SQLAlchemy.
	import os

	os.environ["DATABASE_URL"] = settings.database_url
	reset_database_engine()
	initialize_database()

app = FastAPI(title="TRDIA Backend", version="0.1.0")
install_persistence_error_handler(app)


@app.on_event("startup")
def startup_bootstrap() -> None:
	_bootstrap_persistence()


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(subscriptions_router)
app.include_router(trading_router)
app.include_router(ai_agent_router)
app.include_router(notifications_router)
app.include_router(analytics_router)
