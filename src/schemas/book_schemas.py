from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum
from typing import Literal


class BookStatus(Enum):
    AVAILABLE = 'available'
    DRAFT = 'draft'
    DELETED = 'deleted'


class CreateBookSchema(BaseModel):
    name: str
    author: str
    description: str | None = None
    date_created: date
    url_to_file: str
    price: float = 0.0
    status: Literal['available', 'draft', 'deleted'] = 'draft'


class UpdateBookSchema(BaseModel):
    id: int
    name: str | None = None
    author: str | None = None
    description: str | None = None
    date_created: date | None = None
    url_to_file: str | None = None
    price: float | None = None
    status: Literal['available', 'draft', 'deleted'] | None = None


class BookSchema(BaseModel):
    id: int
    name: str
    author: str
    description: str | None
    date_created: date
    url_to_file: str | None
    price: float
    status: Literal['available', 'draft', 'deleted']
    added_at: datetime
    updated_at: datetime


class BookForUserSchema(BookSchema):
    bought: bool
    in_library: bool


class BookFilter(BaseModel):
    offset: int = 0
    limit: int = 5

    id: int | None = None
    name: str | None = None
    author: str | None = None
    description: str | None = None
    date_created: date | None = None
    url_to_file: str | None = None
    price: float | None = None
    status: Literal['available', 'draft', 'deleted'] | None = None
    added_at: datetime | None = None
    updated_at: datetime | None = None
