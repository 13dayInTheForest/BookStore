from .base_repository import BaseRepository
from src.core.interfaces.user_interface import IUserRepository


class UserRepository(BaseRepository, IUserRepository):
    async def email_check_up(self, user_email: str) -> bool:
        query = self.table.select().where(self.table.c.email == user_email)
        return await self.db.execute(query=query) is not None

