from fastapi import Depends, APIRouter
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from utils.token import create_access_token, get_current_user
from .models import Token
from src.user.models import User, UserPublic, UserResponse
from utils.orm import get_session
from utils.password import verify_password

router = APIRouter()


@router.post("/")
async def auth_login(
    *,
    session: Session = Depends(get_session),
    data: OAuth2PasswordRequestForm = Depends()
):
    db_data = session.exec(select(User).where(User.email == data.username)).first()
    print("\n", db_data, "\n")
    if db_data:
        if verify_password(data.password, db_data.password):
            access_token = create_access_token(data={"sub": db_data.id})
            return Token(access_token=access_token, token_type="bearer")
    return UserResponse(code=404, msg="Data not found")


@router.get("/", response_model=UserPublic)
async def auth_check_login(current_user=Depends(get_current_user)):
    return current_user
