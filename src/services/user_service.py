from fastapi import HTTPException

from src.core.interfaces.user_interface import IUserRepository
from src.schemas.user_schemas import *


class UserService:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def create_user(self, user: CreateUserSchema):
        if await self.repo.email_check_up(user.email) is not None:
            raise HTTPException(status_code=403, detail='Email is Already Registered')
        user_id = int(await self.repo.create(user))

        return await self.repo.read(user_id)

    async def get_user_info(self, user_id: int) -> UserSchema:
        user = await self.repo.read(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail='User Not Found')
        return await self.repo.read(user_id)

    async def update_user(self, updates: UpdateUserSchema):
        user = await self.repo.read(updates.id)
        if user is None:
            raise HTTPException(status_code=404, detail=f'No such User with id-{updates.id}')
        await self.repo.update(updates.id, updates)

        return user

    async def delete_user(self, user_id: int):
        user = await self.repo.read(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail=f'No such User with id-{user_id}')
        await self.repo.delete(user_id)

        return user