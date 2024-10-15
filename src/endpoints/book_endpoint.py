from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from src.schemas.book_schemas import *
from src.schemas.user_schemas import UserSchema, UserRole

from src.db.database import database
from src.core.security import get_current_user
from src.services import BookService, ShelfService, PurchaseService


router = APIRouter(
    prefix='/books'
)


@router.post('/create')
async def create_book(book: CreateBookSchema,
                      user: UserSchema = Depends(get_current_user)):
    if user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail='Forbidden')

    service = BookService(database)
    return await service.create_book(book)


@router.get('/get')
async def show_book_info(book_id: int, user: UserSchema = Depends(get_current_user)):
    shelf_service = ShelfService(database)
    book_service = BookService(database)

    shelf_info = await shelf_service.get_shelf_by_ids(user.id, book_id)
    book_info = await book_service.get_book_info(book_id)

    return BookForUserSchema(
        **book_info.dict(),
        in_library=shelf_info.in_library if shelf_info is not None else False,
        bought=shelf_info is not None
    )


@router.patch('/update')
async def update_book(book_updates: UpdateBookSchema, user: UserSchema = Depends(get_current_user)):
    if user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail='Forbidden')

    service = BookService(database)
    return await service.update_book(book_updates)


@router.delete('/delete')
async def delete_book(book_id: int, user: UserSchema = Depends(get_current_user)):
    if user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail='Forbidden')

    service = BookService(database)
    return await service.delete_book(book_id)


@router.get('/list')
async def get_book_list(
        book_filter: Annotated[BookFilter, Query()]
        ):
    service = BookService(database)
    return await service.get_books_list(book_filter)


@router.post('/buy')
async def buy_book(book_id: int,
                   payment_method: Literal['yandex'],
                   user: UserSchema = Depends(get_current_user)
                   ):
    purchase_service = PurchaseService(database, payment_method)
    return await purchase_service.create_purchase(user.id, book_id)

