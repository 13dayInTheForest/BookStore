from fastapi import APIRouter
from src.schemas.book_schemas import *
from src.db.repositories.book_repository import BookRepository
from src.core.models.books_model import books
from src.db.database import database
from src.services.book_service import BookService


router = APIRouter(
    prefix='/books'
)


@router.post('/create')
async def create_book(book: CreateBookSchema):
    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)

    return await service.create_book(book)


@router.get('/{book_id}')
async def show_book_info(book_id: int):
    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)
    return await service.get_book_info(book_id)


@router.post('/')
async def update_book(book_updates: UpdateBookSchema):
    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)
    return await service.update_user(book_updates)


@router.delete('/delete')
async def delete_book(book_id: int):
    repo = BookRepository(database, books, BookSchema)
    service = BookService(repo)

    return await service.delete_user(book_id)

