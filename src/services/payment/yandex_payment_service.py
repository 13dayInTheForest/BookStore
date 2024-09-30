from src.core.interfaces import IPaymentRepository


class YandexPaymentService(IPaymentRepository):
    async def create_payment_intent(self, amount: float, currency: str = 'usd'):
        return {'payment_id': 'pay1232-csad-213-cdsda'}

    async def check_payment_status(self, payment_intent_id: str):
        return {'status': 'succeeded'}

