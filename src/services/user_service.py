from fastapi import HTTPException

from src.core.interfaces.user_interface import IUserRepository
from src.core.models import users as user_model
from src.db.repositories import UserRepository
from src.schemas.user_schemas import *
from src.core.security import get_password_hash


class UserService:
    def __init__(self, db):
        self.repo: IUserRepository = UserRepository(db, user_model, UserSchema)

    async def create_user(self, user: CreateUserSchema) -> None:
        if await self.repo.email_check_up(user.email):
            raise HTTPException(status_code=403, detail='Email is Already Registered')
        user.password = get_password_hash(user.password)
        await self.repo.create(user)

    async def get_user_info(self, user_id: int) -> UserSchema:
        user = await self.repo.read(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail='User Not Found')
        return await self.repo.read(user_id)

    async def update_user(self, updates: UpdateUserSchema) -> UserSchema:
        user = await self.repo.read(updates.id)
        if user is None:
            raise HTTPException(status_code=404, detail=f'No such User with id-{updates.id}')

        await self.repo.update(updates.id, updates)

        return await self.repo.read(updates.id)

    async def delete_user(self, user_id: int) -> UserSchema:
        user = await self.repo.read(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail=f'No such User with id-{user_id}')
        await self.repo.delete(user_id)

        return user
