from pydantic import BaseModel


class PaymentSchema(BaseModel):
    payment_id: str
    user_id: int
    book_id: int
    price: float


