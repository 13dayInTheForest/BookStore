from sqlalchemy import Table
from src.db.database import database
from pydantic import BaseModel
from typing import TypeVar, Generic, Type


CreateType = TypeVar('CreateType', bound=BaseModel)  # Schema for creating object
UpdateType = TypeVar('UpdateType', bound=BaseModel)  # Schema for updating object
ModelType = TypeVar('ModelType', bound=BaseModel)  # DTO for object
TableType = TypeVar('TableType', bound=Table)  # Table


class BaseRepository(Generic[TableType, ModelType, CreateType, UpdateType]):
    def __init__(self, table: TableType, model: Type[ModelType]):
        self.table = table
        self.model = model

    async def create(self, obj: CreateType) -> int:  # Return User ID
        query = self.table.insert().values(**obj.dict())
        return await database.execute(query=query)

    async def read(self, obj_id: int) -> ModelType:
        query = self.table.select().where(self.table.columns.id == obj_id)
        response = await database.fetch_one(query=query)
        return self.model(**response)

    async def update(self, obj_id: int, obj: UpdateType) -> ModelType:
        query = self.table.update().where(self.table.columns.id == obj_id).values(**obj.dict(exclude_unset=True))
        response = await database.execute(query=query)
        print(response)
        return response

    async def delete(self, obj_id: int) -> bool:
        query = self.table.delete().where(self.table.columns.id == obj_id)
        response = await database.execute(query)
        print(response)
        return response


