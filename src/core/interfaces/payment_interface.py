from abc import ABC, abstractmethod
from src.schemas.payment_schema import CreatePaymentSchema, PaymentSchema


class IPaymentService(ABC):
    @abstractmethod
    async def create_payment_intent(self, new_payment: CreatePaymentSchema) -> PaymentSchema:
        pass

    @abstractmethod
    async def check_payment_status(self, payment: PaymentSchema):
        pass
