from pydantic import BaseModel
from datetime import date, datetime


class ShelfSchema(BaseModel):
    id: int
    user_id: int
    book_id: int
    bought_price: float
    in_library: bool
    date_added: datetime
    last_time_read: datetime


class CreateShelfSchema(BaseModel):
    user_id: int
    book_id: int
    bought_price: float
    in_library: bool = True


class UpdateShelfSchema(BaseModel):
    id: int
    user_id: int | None = None
    book_id: int | None = None
    bought_price: float | None = None
    in_library: bool | None = None
    date_added: datetime | None = None
    last_time_read: datetime | None = None
