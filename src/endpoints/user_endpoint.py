from fastapi import APIRouter
from src.schemas.user_schemas import CreateUserSchema, UpdateUserSchema, UserSchema
from src.db.repositories.user_repository import *
from src.core.models.users_model import users
from src.db.database import database
from src.services.user_service import UserService


router = APIRouter(
    prefix='/user'
)


@router.post('/register')
async def register_user(user: CreateUserSchema):
    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)

    return await service.create_user(user)


@router.get('/profile')
async def get_user_profile(user_id: int):
    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)
    return await service.get_user_info(user_id)


@router.post('/update')
async def update_user(user_updates: UpdateUserSchema):
    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)
    return await service.update_user(user_updates)


@router.delete('/delete')
async def delete_user(user_id: int):
    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)

    return await service.delete_user(user_id)

