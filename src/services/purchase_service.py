from fastapi import HTTPException
from src.core.interfaces import *
from src.core.models import shelf as shelf_model, books as books_model, users as users_model
from src.db.repositories import UserRepository, BookRepository, ShelfRepository

from .payment.yandex_payment_service import YandexPaymentService
from src.schemas.book_schemas import BookStatus, BookSchema
from src.schemas.shelf_schemas import CreateShelfSchema, ShelfSchema
from src.schemas.payment_schema import PaymentSchema, CreatePaymentSchema
from src.schemas.user_schemas import UserSchema



from typing import Literal


class PurchaseService:
    def __init__(self, db, payment_method: Literal['yandex']):
        self.user_repo: IUserRepository = UserRepository(db, users_model, UserSchema)
        self.book_repo: IBookRepository = BookRepository(db, books_model, BookSchema)
        self.shelf_repo: IShelfRepository = ShelfRepository(db, shelf_model, ShelfSchema)

        if payment_method == 'yandex':
            self.payment_service = YandexPaymentService()

    async def create_purchase(self, user_id: int, book_id: int):
        user = await self.user_repo.read(user_id)
        book = await self.book_repo.read(book_id)

        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        if not book:
            raise HTTPException(status_code=404, detail='Book not found')

        if book.status != BookStatus.AVAILABLE.value:
            raise HTTPException(status_code=403, detail='Book Unavailable')

        shelf = await self.shelf_repo.read_by_ids(user_id, book_id)
        if shelf is not None:
            if shelf.in_library:
                raise HTTPException(status_code=409, detail='User has already buy this book')
            else:
                return await self.__return_bought_book_to_library(user_id, book_id)

        if book.price == 0:  # Add book to users shelf if it is free
            return await self.__add_book_to_users_shelf(
                CreateShelfSchema(
                    user_id=user_id,
                    book_id=book_id,
                    bought_price=book.price
                ))

        if user.balance < book.price:
            raise HTTPException(status_code=402, detail='Not enough money to complete the purchase')

        return await self.__create_payment(
            CreatePaymentSchema(
                user_id=user_id,
                book_id=book_id,
                price=book.price
            ))

    async def __create_payment(self, new_payment: CreatePaymentSchema):
        payment = await self.payment_service.create_payment_intent(new_payment)
        payment_info = await self.payment_service.check_payment_status(payment)
        if payment_info['status'] == 'succeeded':
            return await self.__add_book_to_users_shelf(
                CreateShelfSchema(
                    user_id=payment.user_id,
                    book_id=payment.book_id,
                    bought_price=payment.price
                ))

    async def __add_book_to_users_shelf(self, shelf: CreateShelfSchema):
        await self.shelf_repo.create(shelf)
        await self.user_repo.withdraw_money(shelf.user_id, shelf.bought_price)
        return {'detail': 'Book added to User\'s Shelf'}

    async def __return_bought_book_to_library(self, user_id: int, book_id: int):
        await self.shelf_repo.return_book_to_library(user_id, book_id)
        return {'detail': 'Book added to User\'s Shelf'}
