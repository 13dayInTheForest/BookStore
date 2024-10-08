from .base_repository import BaseRepository
from src.core.interfaces.shelf_interface import IShelfRepository
from src.schemas.shelf_schemas import ShelfSchema


class ShelfRepository(BaseRepository, IShelfRepository):
    async def read_by_ids(self, user_id: int, book_id: int) -> ShelfSchema | None:
        query = self.model.select().where(
            self.model.c.user_id == user_id).where(
            self.model.c.book_id == book_id
        )
        shelf = await self.db.fetch_one(query=query)
        return ShelfSchema(**shelf) if shelf is not None else None

    async def delete_by_ids(self, user_id: int, book_id: int):
        query = self.model.delete().where(
            self.model.c.user_id == user_id).where(
            self.model.c.book_id == book_id
        )
        await self.db.fetch_one(query=query)

    async def get_all_user_shelf(self, user_id: int):
        query = f'''
        SELECT b.*
        FROM books b
        JOIN shelf s ON b.id = s.book_id
        WHERE s.user_id = {user_id}
        AND s.in_library
        '''
        return await self.db.fetch_all(query=query)

    async def delete_book_from_library(self, user_id: int, book_id: int):
        query = self.model.update().where(
            self.model.c.user_id == user_id).where(
            self.model.c.book_id == book_id
        ).values(in_library=False)
        await self.db.execute(query=query)

    async def return_book_to_library(self, user_id: int, book_id: int):
        query = self.model.update().where(
            self.model.c.user_id == user_id).where(
            self.model.c.book_id == book_id
        ).values(in_library=True)
        await self.db.execute(query=query)


