from abc import ABC, abstractmethod
from src.schemas.user_schemas import *


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: CreateUserSchema) -> int:  # Return User ID
        pass

    @abstractmethod
    async def read(self, user_id: int) -> UserSchema:
        pass

    @abstractmethod
    async def update(self, user_id: int, user: UpdateUserSchema) -> None:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def email_check_up(self, user_email: str) -> bool:
        pass

    @abstractmethod
    async def withdraw_money(self, user_id: int, count: float) -> float:
        pass
