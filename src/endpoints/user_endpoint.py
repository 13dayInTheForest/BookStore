from fastapi import APIRouter

from src.schemas.user_schemas import CreateUserSchema, UpdateUserSchema, UserSchema
from src.db.repositories.user_repository import UserRepository
from src.core.models.users_model import users
from src.services.user_service import UserService

from src.schemas.shelf_schemas import ShelfSchema
from src.db.repositories.shelf_repository import ShelfRepository
from src.core.models.shelf_model import shelf
from src.services.shelf_service import ShelfService

from src.db.database import database




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


@router.patch('/update')
async def update_user(user_updates: UpdateUserSchema):
    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)
    return await service.update_user(user_updates)


@router.delete('/delete')
async def delete_user(user_id: int):
    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)

    return await service.delete_user(user_id)


@router.get('/my_books')
async def get_all_user_books(user_id: int):
    repo = ShelfRepository(database, shelf, ShelfSchema)
    service = ShelfService(repo)

    return await service.get_all_shelf(user_id)
