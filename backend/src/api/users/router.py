from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/v1/users", tags=["users"])


class UserMeResponse(BaseModel):
    userId: str
    email: EmailStr


@router.get("/me", response_model=UserMeResponse)
def get_me(current_user: dict = Depends(get_current_user)) -> UserMeResponse:
    return UserMeResponse(userId=current_user["id"], email=current_user["email"])
