from fastapi import APIRouter, Depends, HTTPException

from src.schemas.book_schemas import *
from src.schemas.user_schemas import UserSchema, UserRole

from src.db.database import database
from src.core.security import get_current_user
from src.services import get_book_service, get_purchase_service, get_shelf_service, YandexPaymentService


router = APIRouter(
    prefix='/books'
)


@router.post('/create')
async def create_book(book: CreateBookSchema, user: UserSchema = Depends(get_current_user)):
    if user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail='Forbidden')

    service = get_book_service(database)
    return await service.create_book(book)


@router.get('/get')
async def show_book_info(book_id: int, user: UserSchema = Depends(get_current_user)):
    shelf_service = get_shelf_service(database)
    book_service = get_book_service(database)

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

    service = get_book_service(database)
    return await service.update_book(book_updates)


@router.delete('/delete')
async def delete_book(book_id: int, user: UserSchema = Depends(get_current_user)):
    if user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail='Forbidden')

    service = get_book_service(database)
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
                        limit: int = 5,
                        user: UserSchema = Depends(get_current_user)):

    book_filter = BookFilter(id=id, name=name, author=author, description=description,
                             date_created=date_created, url_to_file=url_to_file, price=price,
                             status=status, added_at=added_at, updated_at=updated_at)

    service = get_book_service(database)
    return await service.get_books_list(offset, limit, book_filter)


@router.post('/buy')
async def buy_book(book_id: int, user: UserSchema = Depends(get_current_user)):
    payment_service = YandexPaymentService()
    purchase_service = get_purchase_service(database, payment_service)
    return await purchase_service.create_purchase(user.id, book_id)

