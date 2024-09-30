from abc import ABC, abstractmethod


class IPaymentRepository(ABC):
    @abstractmethod
    async def create_payment_intent(self, amount: float, currency: str = 'usd'):
        pass

    @abstractmethod
    async def check_payment_status(self, payment_intent_id: str):
        pass
