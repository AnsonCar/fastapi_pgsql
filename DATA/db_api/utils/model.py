from bson import ObjectId
from sqlmodel import Field, SQLModel
from datetime import datetime


def get_time() -> str:
    return str(datetime.now())


def generate_object_id() -> str:
    return str(ObjectId())


class ORMModel(SQLModel):
    id: str | None = Field(default=None, primary_key=True)
    created_at: str = Field(default=None)
    updated_at: str = Field(default=None)


class ResponseModel(SQLModel):
    code: int = Field(default=200)
    msg: str = Field(default="")
