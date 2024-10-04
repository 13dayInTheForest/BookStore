from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.schemas.auth_schema import TokenData
from src.schemas.user_schemas import CreateUserSchema, UpdateUserSchema, UserSchema
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
async def get_user_profile(user: UserSchema = Depends(get_current_user)):
    print(user)
    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)
    return await service.get_user_info(user.id)


@router.patch('/update')
async def update_user(user_updates: UpdateUserSchema):
    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)
    return await service.update_user(user_updates)


@router.delete('/delete')
async def delete_user(user_id: int):
    repo = UserRepository(database, users, UserSchema)
    service = UserService(repo)

    return await service.delete_user(user_id)


@router.get('/my_books')
async def get_all_user_books(user_id: int):
    repo = ShelfRepository(database, shelf, ShelfSchema)
    service = ShelfService(repo)

    return {'books': await service.get_all_shelf(user_id)}


@router.delete('/delete_book')
async def delete_book_from_library(user_id: int, book_id: int):
    shelf_service = ShelfService(ShelfRepository(database, shelf, ShelfSchema))

    return await shelf_service.delete_book_from_library(user_id, book_id)
