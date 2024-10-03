from .base_repository import BaseRepository
from src.core.interfaces.user_interface import IUserRepository


class UserRepository(BaseRepository, IUserRepository):
    async def email_check_up(self, user_email: str) -> bool:
        query = self.table.select().where(self.table.c.email == user_email)
        return await self.db.execute(query=query) is not None

    async def withdraw_money(self, user_id: int, count: float) -> float:
        user = await self.read(user_id)
        new_balance = user.balance - count
        query = self.table.update().where(self.table.c.id == user_id).values(
            balance=new_balance
        )
        await self.db.execute(query=query)
        return new_balance
