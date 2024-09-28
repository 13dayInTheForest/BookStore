from src.core.models.users_model import users
from .base_repository import BaseRepository
from src.schemas.book_schemas import BookScheme, UpdateBookScheme, CreateBookScheme


class BookRepository(BaseRepository[users, BookScheme, UpdateBookScheme, CreateBookScheme]):
    pass
