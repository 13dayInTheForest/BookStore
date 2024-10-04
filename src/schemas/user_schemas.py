from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal
from enum import Enum


class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'


class CreateUserSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    age: int | None = None
    balance: float = 0.0


class CreateUserWithRole(CreateUserSchema):
    role: Literal['user', 'admin'] = 'user'


class UpdateUserSchema(BaseModel):
    id: int
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    age: int | None = None
    balance: float | None = None


class UserSchema(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    age: int | None
    balance: float | None
    role: UserRole
    register_at: datetime


class UserInDBSchema(UserSchema):
    password: str
