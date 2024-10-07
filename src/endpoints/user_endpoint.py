from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse

from src.schemas.auth_schema import TokenData
from src.schemas.user_schemas import CreateUserSchema, UpdateUserSchema, UserSchema, UserRole
from src.db.repositories.user_repository import UserRepository
from src.core.models.users_model import users
from src.services.user_service import UserService

from src.schemas.shelf_schemas import ShelfSchema
from src.db.repositories.shelf_repository import ShelfRepository
from src.core.models.shelf_model import shelf
from src.services.shelf_service import ShelfService

from src.core.security import create_access_token, create_refresh_token, get_current_user
from src.db.database import database


router = APIRouter(
    prefix='/user'
)


@router.post('/register')
async def register_user(user: CreateUserSchema):
    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)
    await service.create_user(user)

    access_token = create_access_token(TokenData(sub=user.email, role='user'))
    refresh_token = create_refresh_token(TokenData(sub=user.email, role='user'))

    response = JSONResponse({"access_token": access_token, "token_type": "bearer"}, status_code=200)
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
    )
    return response


@router.get('/profile')
async def get_user_profile(user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')

    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)
    return await service.get_user_info(user_id if user_id else user.id)


@router.patch('/update')
async def update_user(user_updates: UpdateUserSchema, user: UserSchema = Depends(get_current_user)):
    if user_updates.id and user.role == UserRole.USER and user_updates.id != user.id:
        raise HTTPException(status_code=403, detail='Forbidden')

    if user_updates.id is None:
        user_updates.id = user.id

    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)
    return await service.update_user(user_updates)


@router.delete('/delete')
async def delete_user(user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')

    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)

    return await service.delete_user(user_id if user_id else user.id)


@router.get('/my_books')
async def get_all_user_books(user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')

    repo = ShelfRepository(database, shelf, ShelfSchema)
    service = ShelfService(repo)

    return {'books': await service.get_all_shelf(user_id if user_id else user.id)}


@router.delete('/delete_book')
async def delete_book_from_library(book_id: int, user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')

    shelf_service = ShelfService(ShelfRepository(database, shelf, ShelfSchema))
    await shelf_service.delete_book_from_library(user_id if user_id else user.id, book_id)
    return {'detail': 'Book deleted from library'}
