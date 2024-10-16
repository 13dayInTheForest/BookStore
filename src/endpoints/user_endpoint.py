from fastapi import APIRouter, Depends, HTTPException
from src.schemas.user_schemas import CreateUserSchema, UpdateUserSchema, UserSchema, UserRole

from src.core.security import get_current_user, get_tokens_response
from src.db.database import database
from src.services import UserService, ShelfService


router = APIRouter(
    prefix='/user'
)


@router.post('/register')
async def register_user(user: CreateUserSchema):
    service = UserService(database)
    await service.create_user(user)

    return get_tokens_response(user.email, 'user')


@router.get('/profile')
async def get_user_profile(user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')
    if user_id is None:
        user_id = user.id

    service = UserService(database)
    return await service.get_user_info(user_id)


@router.patch('/update')
async def update_user(user_updates: UpdateUserSchema, user: UserSchema = Depends(get_current_user)):
    if user_updates.id and user.role == UserRole.USER and user_updates.id != user.id:
        raise HTTPException(status_code=403, detail='Forbidden')

    if user_updates.id is None:
        user_updates.id = user.id

    service = UserService(database)
    return await service.update_user(user_updates)


@router.delete('/delete')
async def delete_user(user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')
    if user_id is None:
        user_id = user.id

    service = UserService(database)
    return await service.delete_user(user_id)


@router.get('/my_books')
async def get_all_user_books(user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')
    if user_id is None:
        user_id = user.id

    service = ShelfService(database)
    return await service.get_all_shelf(user_id)


@router.delete('/delete_book')
async def delete_book_from_library(book_id: int, user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')
    if user_id is None:
        user_id = user.id

    service = ShelfService(database)
    return await service.delete_book_from_library(user_id, book_id)
