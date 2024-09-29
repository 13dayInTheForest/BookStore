from pydantic import BaseModel
from datetime import date, datetime


class ShelfSchema(BaseModel):
    id: int
    user_id: int
    book_id: int
    bought_price: float
    date_added: datetime
    last_time_read: datetime