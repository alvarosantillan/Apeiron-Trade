from fastapi import APIRouter, HTTPException, status
from jose import JWTError

from schemas.auth.schemas import (
    FacebookOAuthRequest,
    GoogleOAuthRequest,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    TokenPairResponse,
)
from services.auth.login_protection import login_protection
from services.auth.oauth_user_service import OAuthTokenError, login_with_facebook, login_with_google
from services.auth.session_service import create_session, is_valid_session, revoke_all_sessions, revoke_session
from services.auth.token_service import create_access_token, create_refresh_token, decode_token
from services.audit.auth_audit import auth_audit
from services.auth.user_store import store

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> RegisterResponse:
    try:
        user = store.create_user(payload.email, payload.password)
    except ValueError:
        auth_audit.log(action="register", email=payload.email, outcome="failure")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")
    auth_audit.log(action="register", user_id=user["id"], email=user["email"], outcome="success")
    return RegisterResponse(userId=user["id"], email=user["email"])


@router.post("/login", response_model=TokenPairResponse)
def login(payload: LoginRequest) -> TokenPairResponse:
    if not login_protection.can_attempt(payload.email):
        auth_audit.log(action="login", email=payload.email, outcome="blocked")
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="too many failed attempts")

    user = store.authenticate(payload.email, payload.password)
    if not user:
        login_protection.register_failure(payload.email)
        auth_audit.log(action="login", email=payload.email, outcome="failure")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    login_protection.register_success(payload.email)
    auth_audit.log(action="login", user_id=user["id"], email=user["email"], outcome="success")

    access_token = create_access_token(user["id"], user["email"])
    refresh_token = create_refresh_token(user["id"])
    create_session(user["id"], refresh_token)

    return TokenPairResponse(accessToken=access_token, refreshToken=refresh_token)


@router.post("/refresh", response_model=TokenPairResponse)
def refresh(payload: RefreshRequest) -> TokenPairResponse:
    try:
        decoded = decode_token(payload.refreshToken)
        user_id = decoded["sub"]
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type")
    except JWTError:
        auth_audit.log(action="refresh", outcome="failure")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")

    if not is_valid_session(user_id, payload.refreshToken):
        auth_audit.log(action="refresh", user_id=user_id, outcome="failure")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token revoked")

    revoke_session(user_id, payload.refreshToken)
    access_token = create_access_token(user_id, "")
    refresh_token = create_refresh_token(user_id)
    create_session(user_id, refresh_token)
    auth_audit.log(action="refresh", user_id=user_id, outcome="success")
    return TokenPairResponse(accessToken=access_token, refreshToken=refresh_token)


@router.post("/oauth/google", response_model=TokenPairResponse)
def oauth_google(payload: GoogleOAuthRequest) -> TokenPairResponse:
    try:
        tokens = login_with_google(payload.idToken)
    except OAuthTokenError:
        auth_audit.log(action="oauth_google", outcome="failure")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid oauth token")
    auth_audit.log(action="oauth_google", outcome="success")
    return TokenPairResponse(**tokens)


@router.post("/oauth/facebook", response_model=TokenPairResponse)
def oauth_facebook(payload: FacebookOAuthRequest) -> TokenPairResponse:
    try:
        tokens = login_with_facebook(payload.accessToken)
    except OAuthTokenError:
        auth_audit.log(action="oauth_facebook", outcome="failure")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid oauth token")
    auth_audit.log(action="oauth_facebook", outcome="success")
    return TokenPairResponse(**tokens)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: LogoutRequest) -> None:
    try:
        decoded = decode_token(payload.refreshToken)
        user_id = decoded["sub"]
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type")
    except JWTError:
        auth_audit.log(action="logout", outcome="failure")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")

    revoke_session(user_id, payload.refreshToken)
    auth_audit.log(action="logout", user_id=user_id, outcome="success")


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
def logout_all(payload: LogoutRequest) -> None:
    try:
        decoded = decode_token(payload.refreshToken)
        user_id = decoded["sub"]
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token type")
    except JWTError:
        auth_audit.log(action="logout_all", outcome="failure")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")

    revoke_all_sessions(user_id)
    auth_audit.log(action="logout_all", user_id=user_id, outcome="success")
