from .book_service import BookService
from .purchase_service import PurchaseService
from .shelf_service import ShelfService
from .user_service import UserService
from .payment.yandex_payment_service import YandexPaymentService

from src.db.repositories.user_repository import UserRepository
from src.db.repositories.book_repository import BookRepository
from src.db.repositories.shelf_repository import ShelfRepository

from src.schemas.user_schemas import UserSchema
from src.schemas.book_schemas import BookSchema
from src.schemas.shelf_schemas import ShelfSchema

from src.core.models.users_model import users
from src.core.models.books_model import books
from src.core.models.shelf_model import shelf

from src.core.interfaces.payment_interface import IPaymentService


__all__ = [
    'get_user_service',
    'get_book_service',
    'get_shelf_service',
    'get_purchase_service',
    'YandexPaymentService'
]


def get_user_service(db) -> UserService:
    return UserService(UserRepository(db, users, UserSchema))


def get_book_service(db) -> BookService:
    return BookService(BookRepository(db, books, BookSchema))


def get_shelf_service(db) -> ShelfService:
    return ShelfService(ShelfRepository(db, shelf, ShelfSchema))


def get_purchase_service(db, payment_service: IPaymentService) -> PurchaseService:
    return PurchaseService(
        UserRepository(db, users, UserSchema),
        BookRepository(db, books, BookSchema),
        ShelfRepository(db, shelf, ShelfSchema),
        payment_service
        )
