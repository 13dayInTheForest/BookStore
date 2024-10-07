from sqlalchemy import Table
from pydantic import BaseModel
from typing import Type


class BaseRepository:
    def __init__(self, db, model: Type[Table], schema: Type[BaseModel]):
        self.db = db
        self.model = model
        self.schema = schema

    async def create(self, obj: Type[BaseModel]) -> int:  # Return Obj ID
        query = self.model.insert().values(**obj.dict())
        print(query)
        return await self.db.execute(query=query)

    async def read(self, obj_id: int) -> Type[BaseModel] | None:
        query = self.model.select().where(self.model.columns.id == obj_id)
        response = await self.db.fetch_one(query=query)
        return self.schema(**response) if response is not None else None

    async def update(self, obj_id: int, obj: Type[BaseModel]) -> None:
        query = self.model.update().where(
            self.model.columns.id == obj_id).values(**obj.dict(exclude_unset=True, exclude_none=True)
                                                    )
        await self.db.execute(query=query)

    async def delete(self, obj_id: int) -> None:
        query = self.model.delete().where(self.model.columns.id == obj_id)
        await self.db.execute(query)



