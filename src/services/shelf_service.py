from fastapi import HTTPException

from src.core.interfaces.shelf_interface import IShelfRepository
from src.schemas.shelf_schemas import *


class ShelfService:
    def __init__(self, repo: IShelfRepository):
        self.repo = repo

    async def create_shelf(self, shelf: CreateShelfSchema):
        if await self.repo.read_by_ids(shelf.user_id, shelf.book_id) is not None:
            raise HTTPException(status_code=403, detail='Book is Already In Shelf')
        shelf_id = await self.repo.create(shelf)

        return await self.repo.read(shelf_id)

    async def get_shelf(self, shelf_id: int) -> ShelfSchema:
        shelf = await self.repo.read(shelf_id)
        if shelf is None:
            raise HTTPException(status_code=404, detail='Shelf Not Found')
        return await self.repo.read(shelf_id)

    async def update_shelf(self, updates: UpdateShelfSchema):
        shelf = await self.repo.read(updates.id)
        if shelf is None:
            raise HTTPException(status_code=404, detail=f'No such Shelf with id-{updates.id}')
        await self.repo.update(updates.id, updates)

        return await self.repo.read(updates.id)

    async def delete_shelf(self, shelf_id: int):
        user = await self.repo.read(shelf_id)

        if user is None:
            raise HTTPException(status_code=404, detail=f'No such Shelf with id-{shelf_id}')
        await self.repo.delete(shelf_id)

        return user

    async def get_all_shelf(self, user_id: int):
        shelf = await self.repo.get_all_user_shelf(user_id)
        return shelf
