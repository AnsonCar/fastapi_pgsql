from fastapi import Depends, APIRouter
from sqlmodel import Session, select
from .models import *
from utils.orm import get_session
from utils.model import generate_object_id, get_time
from utils.password import hash_password

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_User(*, session: Session = Depends(get_session), data: UserCreate):
    db_data = session.exec(select(User).where(User.email == data.email)).first()
    if db_data:
        return UserResponse(code=400, msg="User with this email already exists")
    hashed_password = hash_password(data.password)
    extra_data = {"password": hashed_password}
    db_data = User.model_validate(data, update=extra_data)
    db_data.id = generate_object_id()
    db_data.created_at = get_time()
    db_data.updated_at = get_time()
    session.add(db_data)
    session.commit()
    session.refresh(db_data)
    return UserResponse(code=200, data=db_data, msg="Add Successfully.")


@router.get("/", response_model=UserResponse)
async def read_Users(*, session: Session = Depends(get_session)):
    db_data = session.exec(select(User)).all()
    return UserResponse(code=200, data=db_data, msg="Gets Successfully.")


@router.get("/{id}", response_model=UserResponse)
async def read_User(*, session: Session = Depends(get_session), id: str):
    db_data = session.get(User, id)
    if not db_data:
        return UserResponse(code=404, msg="Data not found")
    return UserResponse(code=200, data=db_data, msg="Get Successfully.")


@router.patch("/{id}", response_model=UserResponse)
async def update_User(
    *, session: Session = Depends(get_session), id: str, data: UserUpdate
):
    db_data = session.get(User, id)
    if not db_data:
        return UserResponse(code=404, msg="Data not found")
    data = data.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_data, key, value)
    setattr(db_data, "updated_at", get_time())
    session.add(db_data)
    session.commit()
    session.refresh(db_data)
    return UserResponse(code=200, data=db_data, msg="Get Successfully.")


@router.delete("/{id}")
async def delete_User(*, session: Session = Depends(get_session), id: str):
    data = session.get(User, id)
    if not data:
        return UserResponse(code=404, msg="Data not found")
    session.delete(data)
    session.commit()
    return UserResponse(code=200, msg="Delete Successfully.")
