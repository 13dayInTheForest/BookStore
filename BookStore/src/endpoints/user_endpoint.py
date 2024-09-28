from fastapi import APIRouter
from src.schemas.user_schemas import CreateUserScheme, UpdateUserScheme
from src.db.repositories.user_repository import UserRepository
from src.core.models.users_model import users


router = APIRouter(
    prefix='/user'
)


@router.post('/register')
async def register_user(user: CreateUserScheme):
    repo = UserRepository(users, CreateUserScheme)
    return await repo.create(user)


@router.get('/profile')
async def get_user_profile(user_id: int):
    repo = UserRepository(users, CreateUserScheme)
    return await repo.read(user_id)


@router.post('/update')
async def update_user(user_updates: UpdateUserScheme):
    repo = UserRepository(users, CreateUserScheme)
    user_id = user_updates.id
    return await repo.update(user_id, user_updates)

