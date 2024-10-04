from sqlalchemy import Table
from pydantic import BaseModel
from typing import Type


class BaseRepository:
    def __init__(self, db, table: Type[Table], model: Type[BaseModel]):
        self.db = db
        self.table = table
        self.model = model

    async def create(self, obj: Type[BaseModel]) -> int:  # Return Obj ID
        query = self.table.insert().values(**obj.dict())
        print(query)
        return await self.db.execute(query=query)

    async def read(self, obj_id: int) -> Type[BaseModel] | None:
        query = self.table.select().where(self.table.columns.id == obj_id)
        response = await self.db.fetch_one(query=query)
        return self.model(**response) if response is not None else None

    async def update(self, obj_id: int, obj: Type[BaseModel]) -> None:
        query = self.table.update().where(self.table.columns.id == obj_id).values(**obj.dict(exclude_unset=True))
        await self.db.execute(query=query)

    async def delete(self, obj_id: int) -> None:
        query = self.table.delete().where(self.table.columns.id == obj_id)
        await self.db.execute(query)



