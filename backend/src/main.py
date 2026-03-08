from fastapi import FastAPI

from api.auth.router import router as auth_router
from api.users.router import router as users_router

app = FastAPI(title="TRDIA Backend", version="0.1.0")
app.include_router(auth_router)
app.include_router(users_router)
