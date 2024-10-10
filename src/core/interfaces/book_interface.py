from abc import ABC, abstractmethod
from src.schemas.book_schemas import *


class IBookRepository(ABC):
    @abstractmethod
    async def create(self, book: CreateBookSchema) -> int:
        pass

    @abstractmethod
    async def read(self, book_id: int) -> BookSchema:
        pass

    @abstractmethod
    async def update(self, book_id: int, user: UpdateBookSchema) -> None:
        pass

    @abstractmethod
    async def delete(self, book_id: int) -> None:
        pass

    @abstractmethod
    async def exists_book_check(self, author_name: str, book_name: str) -> bool:
        pass

    @abstractmethod
    async def get_book_list(self, offset: int, limit: int, book_filter: BookFilter):
        pass

