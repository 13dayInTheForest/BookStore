from src.core.models.users_model import users
from .base_repository import BaseRepository
from src.core.interfaces.book_interface import IBookRepository


class BookRepository(BaseRepository, IBookRepository):
    async def exists_book_check(self, author_name: str, book_name: str) -> bool:
        query = self.table.select().where(self.table.c.name == book_name).where(self.table.c.author == author_name)
        return await self.db.execute(query=query)