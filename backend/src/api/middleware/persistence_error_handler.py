from __future__ import annotations

from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from services.persistence.errors import PersistenceError, PersistenceUnavailableError


def install_persistence_error_handler(app: FastAPI) -> None:
    @app.exception_handler(PersistenceUnavailableError)
    async def _unavailable_handler(_: Request, exc: PersistenceUnavailableError) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content={"code": exc.code, "message": str(exc), "traceId": str(uuid4())},
        )

    @app.exception_handler(PersistenceError)
    async def _transaction_handler(_: Request, exc: PersistenceError) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content={"code": exc.code, "message": str(exc), "traceId": str(uuid4())},
        )
