from .base_repository import BaseRepository
from src.core.interfaces.user_interface import IUserRepository
from src.schemas.user_schemas import CreateUserSchema, CreateUserWithRole


class UserRepository(BaseRepository, IUserRepository):
    async def create(self, user: CreateUserSchema) -> int:
        user = CreateUserWithRole(**user.dict())
        query = self.model.insert().values(**user.dict())
        return await self.db.execute(query=query)

    async def email_check_up(self, user_email: str) -> bool:
        query = self.model.select().where(self.model.c.email == user_email)
        return await self.db.execute(query=query) is not None

    async def withdraw_money(self, user_id: int, count: float) -> float:
        user = await self.read(user_id)
        new_balance = user.balance - count
        query = self.model.update().where(self.model.c.id == user_id).values(
            balance=new_balance
        )
        await self.db.execute(query=query)
        return new_balance
