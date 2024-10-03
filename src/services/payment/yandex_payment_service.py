from src.core.interfaces import IPaymentService
from src.schemas.payment_schema import CreatePaymentSchema, PaymentSchema


class YandexPaymentService(IPaymentService):
    async def create_payment_intent(self, new_payment: CreatePaymentSchema):
        return PaymentSchema(payment_id='pay1232-csad-213-cdsda', **new_payment.dict())

    async def check_payment_status(self, payment: PaymentSchema):
        return {'status': 'succeeded'}

