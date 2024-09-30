from .base_repository import BaseRepository
from src.core.interfaces.shelf_interface import IShelfRepository


class ShelfRepository(BaseRepository, IShelfRepository):
    async def read_by_ids(self, user_id: int, book_id: int) -> bool:
        query = self.table.select().where(self.table.c.user_id == user_id).where(self.table.c.book_id == book_id)
        return await self.db.execute(query=query) is not None

    async def get_all_user_shelf(self, user_id: int):
        query = self.table.select().where(self.table.c.user_id == user_id)

        return await self.db.fetch_all(query=query)
