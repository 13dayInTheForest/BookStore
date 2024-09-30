from fastapi import HTTPException
from src.core.interfaces import *
from src.schemas.book_schemas import BookStatus
from src.schemas.shelf_schemas import CreateShelfSchema
from src.schemas.payment_schema import PaymentSchema


class PurchaseService:
    def __init__(self,
                 user_repo: IUserRepository,
                 book_repo: IBookRepository,
                 shelf_repo: IShelfRepository,
                 payment_repo: IPaymentRepository
                 ):
        self.user_repo = user_repo
        self.book_repo = book_repo
        self.shelf_repo = shelf_repo
        self.payment_repo = payment_repo

    async def create_purchase(self, user_id: int, book_id: int):
        user = await self.user_repo.read(user_id)
        book = await self.book_repo.read(book_id)

        if user:
            raise HTTPException(status_code=404, detail='User not found')

        if book:
            raise HTTPException(status_code=404, detail='Book not found')

        if await self.shelf_repo.read_by_ids(user_id, book_id):
            raise HTTPException(status_code=409, detail='User has already purchased this book')

        if book.status != BookStatus.AVAILABLE.value:
            raise HTTPException(status_code=403, detail='Book Unavailable')

        if book.price == 0: # Add book to users shelf if it is free
            await self.shelf_repo.create(CreateShelfSchema(user_id=user_id, book_id=book_id, bought_price=book.price))

        if user.balance < book.price:
            raise HTTPException(status_code=402, detail='Not enough funds to complete the purchase')
        payment_id = await self.payment_repo.create_payment_intent(book.price, 'usd')

        return PaymentSchema(payment_id=payment_id, user_id=user_id, book_id=book_id, price=book.price)

    async def check_payment(self, p: PaymentSchema):
        payment_status = await self.payment_repo.check_payment_status(p.payment_id)

        if payment_status['status'] != 'succeeded':
            raise HTTPException(status_code=402, detail='Payment not made')

        shelf_id = await self.shelf_repo.create(
            CreateShelfSchema(user_id=p.user_id, book_id=p.book_id, bought_price=p.price)
        )

        return await self.shelf_repo.read(shelf_id)

