from abc import ABC, abstractmethod
from src.schemas.book_schemas import *


class IBookRepository(ABC):
    @abstractmethod
    async def create(self, user: CreateBookSchema) -> int:  # Return User ID
        pass

    @abstractmethod
    async def read(self, user_id: int) -> BookSchema:
        pass

    @abstractmethod
    async def update(self, user_id: int, user: UpdateBookSchema) -> None:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def exists_book_check(self, author_name: str, book_name: str) -> bool:
        pass

