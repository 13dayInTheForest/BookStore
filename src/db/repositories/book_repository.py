from src.core.models.users_model import users
from .base_repository import BaseRepository
from src.core.interfaces.book_interface import IBookRepository
from src.schemas.book_schemas import BookFilter


class BookRepository(BaseRepository, IBookRepository):
    async def exists_book_check(self, author_name: str, book_name: str) -> bool:
        query = self.table.select().where(self.table.c.name == book_name).where(self.table.c.author == author_name)
        return await self.db.execute(query=query) is not None

    async def get_book_list(self, offset: int, limit: int, book_filter: BookFilter):
        query = self.table.select().filter_by(**book_filter.dict(exclude_none=True)).limit(limit).offset(offset)
        return await self.db.fetch_all(query=query)
