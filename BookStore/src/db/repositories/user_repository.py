from src.core.models.users_model import users
from .base_repository import BaseRepository
from src.schemas.user_schemas import UserScheme, UpdateUserScheme, CreateUserScheme


class UserRepository(BaseRepository[users, UserScheme, CreateUserScheme, UpdateUserScheme]):
    pass
