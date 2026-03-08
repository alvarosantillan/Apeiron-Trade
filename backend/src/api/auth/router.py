from fastapi import APIRouter, HTTPException, status
from jose import JWTError, jwt

from schemas.auth.schemas import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    TokenPairResponse,
)
from services.auth.token_service import ALGORITHM, SECRET_KEY, create_access_token, create_refresh_token
from services.auth.user_store import store

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> RegisterResponse:
    try:
        user = store.create_user(payload.email, payload.password)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")
    return RegisterResponse(userId=user["id"], email=user["email"])


@router.post("/login", response_model=TokenPairResponse)
def login(payload: LoginRequest) -> TokenPairResponse:
    user = store.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    access_token = create_access_token(user["id"], user["email"])
    refresh_token = create_refresh_token(user["id"])
    store.save_refresh_token(user["id"], refresh_token)

    return TokenPairResponse(accessToken=access_token, refreshToken=refresh_token)


@router.post("/refresh", response_model=TokenPairResponse)
def refresh(payload: RefreshRequest) -> TokenPairResponse:
    try:
        decoded = jwt.decode(payload.refreshToken, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded["sub"]
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")

    if not store.validate_refresh_token(user_id, payload.refreshToken):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token revoked")

    access_token = create_access_token(user_id, "")
    refresh_token = create_refresh_token(user_id)
    store.save_refresh_token(user_id, refresh_token)
    return TokenPairResponse(accessToken=access_token, refreshToken=refresh_token)
