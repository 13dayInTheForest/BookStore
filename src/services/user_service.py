from typing import Annotated

from fastapi import HTTPException, Depends

from src.core.interfaces.user_interface import IUserRepository
from src.core.models import users
from src.db.repositories.user_repository import UserRepository

from src.schemas.user_schemas import *
from src.core.security import get_password_hash, get_current_user


class UserService:
    def __init__(self, db):
        self.repo: IUserRepository = UserRepository(db, users, UserSchema)

    async def create_user(self, new_user: CreateUserSchema) -> None:
        if await self.repo.email_check_up(new_user.email):
            raise HTTPException(status_code=403, detail='Email is Already Registered')

        new_user.password = get_password_hash(new_user.password)
        user_id = await self.repo.create(new_user)
        await self.repo.read(user_id)

    async def get_user_info(self, user_id: int | None = None,
                            user: UserSchema = Depends(get_current_user)
                            ) -> UserSchema:
        if user_id and user.role == UserRole.USER and user.id != user_id:
            raise HTTPException(status_code=403, detail='Forbidden')
        if user_id is None:
            user_id = user.id

        user = await self.repo.read(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail='User Not Found')
        return await self.repo.read(user_id)

    async def update_user(self, updates: UpdateUserSchema,
                          user: UserSchema = Depends(get_current_user)
                          ):
        if updates.id and user.role == UserRole.USER and updates.id != user.id:
            raise HTTPException(status_code=403, detail='Forbidden')
        if updates.id is None:
            updates.id = user.id

        user = await self.repo.read(updates.id)
        if user is None:
            raise HTTPException(status_code=404, detail=f'No such User with id-{updates.id}')

        await self.repo.update(updates.id, updates)
        return await self.repo.read(updates.id)

    async def delete_user(self, user_id: int | None = None,
                          user: UserSchema = Depends(get_current_user)
                          ):
        if user_id and user.role == UserRole.USER and user.id != user_id:
            raise HTTPException(status_code=403, detail='Forbidden')
        if user_id is None:
            user_id = user.id

        user = await self.repo.read(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail=f'No such User with id-{user_id}')
        await self.repo.delete(user_id)

        return user
