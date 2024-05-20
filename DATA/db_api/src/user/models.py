from sqlmodel import Field, SQLModel
from utils.model import ORMModel, ResponseModel


# For DB
class User(ORMModel, table=True):
    __tablename__ = "user"

    email: str = Field(index=True, unique=True)
    password: str = Field()


# For API
class UserPublic(ORMModel):
    email: str = Field(index=True, unique=True)


class UserResponse(ResponseModel):
    data: list[UserPublic] | UserPublic | None = None


# For API Post Put
class UserCreate(SQLModel):
    email: str = Field(index=True, unique=True)
    password: str


class UserUpdate(SQLModel):
    email: str | None = None
