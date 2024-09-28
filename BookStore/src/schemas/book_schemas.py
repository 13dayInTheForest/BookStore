from pydantic import BaseModel
from datetime import datetime
from typing import Literal
from enum import Enum


class BookStatus(Enum):
    AVAILABLE = 'available'
    DRAFT = 'draft'
    DELETED = 'deleted'


class CreateBookScheme(BaseModel):
    name: str
    author: str
    description: str = None
    date_created: datetime
    price: float = 0.0
    status: BookStatus = BookStatus.DRAFT


class UpdateBookScheme(BaseModel):
    id: int
    name: str | None = None
    author: str | None = None
    description: str | None = None
    date_created: datetime | None = None
    price: float | None = None
    status: BookStatus | None = None


class BookScheme(BaseModel):
    id: int
    name: str
    author: str
    description: str
    date_created: datetime
    price: float
    status: BookStatus
    added_at: datetime
    updated_at: datetime


