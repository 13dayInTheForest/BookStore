from pydantic import BaseModel
from datetime import datetime


class CreateUserSchema(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    age: int | None = None
    balance: float = 0.0


class UpdateUserSchema(BaseModel):
    id: int
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    password: str | None = None
    age: int | None = None
    balance: float | None = None


class UserSchema(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    password: str
    age: int | None
    balance: float | None
    register_at: datetime


