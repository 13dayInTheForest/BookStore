from fastapi import HTTPException

from src.core.interfaces.book_interface import IBookRepository
from src.core.interfaces.shelf_interface import IShelfRepository
from src.schemas.book_schemas import *


class BookService:
    def __init__(self, repo: IBookRepository):
        self.repo = repo

    async def create_book(self, book: CreateBookSchema):
        if await self.repo.exists_book_check(book.author, book.name):
            raise HTTPException(status_code=403, detail='Book is Already In Library')
        book_id = await self.repo.create(book)

        return await self.repo.read(book_id)

    async def get_book_info(self, book_id: int) -> BookSchema:
        book = await self.repo.read(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail=f'No such Book with id-{book_id}')
        return book

    async def get_personalized_book_info(self,
                                         user_id: int,
                                         book_id: int,
                                         shelf_repo: IShelfRepository
                                         ) -> BookForUserSchema:
        book = await self.get_book_info(book_id)
        shelf_info = await shelf_repo.read_by_ids(user_id, book_id)
        if shelf_info is not None:
            book_info = BookForUserSchema(bought=shelf_info is not None,
                                          in_library=shelf_info.in_library,
                                          **book.dict())
        else:
            book_info = BookForUserSchema(bought=False, in_library=False, **book.dict())

        return book_info

    async def update_book(self, updates: UpdateBookSchema):
        book = await self.repo.read(updates.id)
        if book is None:
            raise HTTPException(status_code=404, detail=f'No such Book with id-{updates.id}')
        await self.repo.update(updates.id, updates)

        return await self.repo.read(updates.id)

    async def delete_book(self, book_id: int):
        book = await self.repo.read(book_id)

        if book is None:
            raise HTTPException(status_code=404, detail=f'No such Book with id-{book_id}')
        await self.repo.delete(book_id)

        return book

    async def get_books_list(self, offset: int, limit: int, books_filter: BookFilter):
        book_list = await self.repo.get_book_list(offset, limit, books_filter)
        return book_list
