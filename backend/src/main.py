from fastapi import FastAPI

from api.auth.router import router as auth_router

app = FastAPI(title="TRDIA Backend", version="0.1.0")
app.include_router(auth_router)
