from contextlib import asynccontextmanager
import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


logger = logging.getLogger(__name__)


def _allowed_origins() -> list[str]:
	origins_env = os.getenv("CORS_ALLOW_ORIGINS", "")
	if origins_env.strip():
		return [origin.strip() for origin in origins_env.split(",") if origin.strip()]

	# Defaults for local container-first workflow.
	return [
		"http://localhost:5111",
		"http://127.0.0.1:5111",
		"http://localhost:5173",
		"http://127.0.0.1:5173",
		"http://localhost:3111",
		"http://127.0.0.1:3111",
	]


def _bootstrap_persistence() -> None:
	settings = load_db_settings()
	# Keep a single source of truth for database URL used by SQLAlchemy.
	os.environ["DATABASE_URL"] = settings.database_url
	reset_database_engine()
	initialize_database()


@asynccontextmanager
async def lifespan(_: FastAPI):
	logger.info("startup initialized")
	_bootstrap_persistence()
	try:
		yield
	finally:
		logger.info("shutdown completed")


app = FastAPI(title="TRDIA Backend", version="0.1.0", lifespan=lifespan)
app.add_middleware(
	CORSMiddleware,
	allow_origins=_allowed_origins(),
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
install_persistence_error_handler(app)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(subscriptions_router)
app.include_router(trading_router)
app.include_router(ai_agent_router)
app.include_router(notifications_router)
app.include_router(analytics_router)
