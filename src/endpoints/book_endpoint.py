from fastapi import APIRouter, Depends, HTTPException
from src.schemas.book_schemas import *
from src.schemas.user_schemas import UserSchema, UserRole
from src.schemas.shelf_schemas import ShelfSchema
from src.db.repositories import BookRepository, UserRepository, ShelfRepository
from src.core.models import *
from src.db.database import database
from src.services import BookService, PurchaseService, YandexPaymentService
from src.core.security import get_current_user

router = APIRouter(
    prefix='/books'
)


@router.post('/create', response_model=BaseModel)
async def create_book(book: CreateBookSchema, user: UserSchema = Depends(get_current_user)):
    if user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail='Forbidden')

    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)

    return await service.create_book(book)


@router.get('/get')
async def show_book_info(book_id: int, user: UserSchema = Depends(get_current_user)):
    book_repo = BookRepository(database, books, BookSchema)
    shelf_repo = ShelfRepository(database, shelf, ShelfSchema)
    book_service = BookService(book_repo)

    return await book_service.get_personalized_book_info(user.id, book_id, shelf_repo)


@router.patch('/update')
async def update_book(book_updates: UpdateBookSchema, user: UserSchema = Depends(get_current_user)):
    if user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail='Forbidden')

    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)

    return await service.update_book(book_updates)


@router.delete('/delete')
async def delete_book(book_id: int, user: UserSchema = Depends(get_current_user)):
    if user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail='Forbidden')

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
                        limit: int = 5,
                        user: UserSchema = Depends(get_current_user)):

    book_filter = BookFilter(id=id, name=name, author=author, description=description,
                             date_created=date_created, url_to_file=url_to_file, price=price,
                             status=status, added_at=added_at, updated_at=updated_at)

    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)
    return await service.get_books_list(offset, limit, book_filter)


@router.post('/buy')
async def buy_book(book_id: int, user: UserSchema = Depends(get_current_user)):
    purchase_service = PurchaseService(
        UserRepository(database, users, UserSchema),
        BookRepository(database, books, BookSchema),
        ShelfRepository(database, shelf, ShelfSchema),
        YandexPaymentService()
    )
    return await purchase_service.create_purchase(user.id, book_id)

