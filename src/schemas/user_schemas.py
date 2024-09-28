from pydantic import BaseModel
from datetime import datetime


class CreateUserScheme(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    age: int | None = None


class UpdateUserScheme(BaseModel):
    id: int
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    password: str | None = None
    age: int | None = None
    balance: float | None = None


class UserScheme(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    password: str
    age: int | None = None
    balance: float
    register_at: datetime


