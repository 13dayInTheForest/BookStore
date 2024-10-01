from fastapi import APIRouter, Query
from src.schemas.book_schemas import *
from src.schemas.user_schemas import UserSchema, UpdateUserSchema
from src.schemas.shelf_schemas import ShelfSchema
from src.schemas.payment_schema import PaymentSchema
from src.db.repositories import BookRepository, UserRepository, ShelfRepository
from src.core.models import *
from src.db.database import database
from src.services import BookService, PurchaseService, YandexPaymentService
from typing import Annotated


router = APIRouter(
    prefix='/books'
)


@router.post('/create')
async def create_book(book: CreateBookSchema):
    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)

    return await service.create_book(book)


@router.get('/get')
async def show_book_info(book_id: int):
    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)

    return await service.get_book_info(book_id)


@router.patch('/update')
async def update_book(book_updates: UpdateBookSchema):
    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)

    return await service.update_book(book_updates)


@router.delete('/delete')
async def delete_book(book_id: int):
    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)

    return await service.delete_book(book_id)


@router.get('/list')
async def get_book_list(id: int | None = None,
                        name: str | None = None,
                        author: str | None = None,
                        description: str | None = None,
                        date_created: date | None = None,
                        url_to_file: str | None = None,
                        price: float | None = None,
                        status: Literal['available', 'draft', 'deleted'] | None = None,
                        added_at: datetime | None = None,
                        updated_at: datetime | None = None,
                        offset: int = 0,
                        limit: int = 5):

    book_filter = BookFilter(id=id, name=name, author=author, description=description,
                             date_created=date_created, url_to_file=url_to_file, price=price,
                             status=status, added_at=added_at, updated_at=updated_at)

    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)
    return await service.get_books_list(offset, limit, book_filter)


@router.post('/create_payment')
async def buy_book(user_id: int, book_id: int):
    book_repo = BookRepository(database, books, BookSchema)
    user_repo = UserRepository(database, users, UserSchema)
    shelf_repo = ShelfRepository(database, shelf, ShelfSchema)
    purchase_service = PurchaseService(user_repo, book_repo, shelf_repo, YandexPaymentService())

    return await purchase_service.create_purchase(user_id, book_id)


@router.get('/check_payment')
async def check_payment(payment: Annotated[PaymentSchema, Query(...)]):
    book_repo = BookRepository(database, books, BookSchema)
    user_repo = UserRepository(database, users, UserSchema)
    shelf_repo = ShelfRepository(database, shelf, ShelfSchema)
    purchase_service = PurchaseService(user_repo, book_repo, shelf_repo, YandexPaymentService())
    await purchase_service.check_payment(payment)

    return
