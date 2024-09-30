from abc import ABC, abstractmethod
from src.schemas.shelf_schemas import *


class IShelfRepository(ABC):
    @abstractmethod
    async def create(self, shelf: CreateShelfSchema) -> int:
        pass

    @abstractmethod
    async def read(self, shelf_id: int) -> ShelfSchema:
        pass

    @abstractmethod
    async def update(self, shelf_id: int, user: UpdateShelfSchema) -> None:
        pass

    @abstractmethod
    async def delete(self, shelf_id: int) -> None:
        pass

    @abstractmethod
    async def read_by_ids(self, user_id: int, book_id: int) -> bool:
        pass

    @abstractmethod
    async def get_all_user_shelf(self, user_id: int):
        pass
