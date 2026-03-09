from fastapi import FastAPI

from api.auth.router import router as auth_router
from api.subscriptions.router import router as subscriptions_router
from api.trading.router import router as trading_router
from api.users.router import router as users_router

app = FastAPI(title="TRDIA Backend", version="0.1.0")
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(subscriptions_router)
app.include_router(trading_router)
