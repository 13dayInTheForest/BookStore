from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.services import get_user_service, get_shelf_service

from src.schemas.auth_schema import TokenData
from src.schemas.user_schemas import CreateUserSchema, UpdateUserSchema, UserSchema, UserRole

from src.core.security import create_access_token, create_refresh_token, get_current_user
from src.db.database import database


router = APIRouter(
    prefix='/user'
)


@router.post('/register')
async def register_user(user: CreateUserSchema):
    service = get_user_service(database)
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

    service = get_user_service(database)
    return await service.get_user_info(user_id if user_id else user.id)


@router.patch('/update')
async def update_user(user_updates: UpdateUserSchema, user: UserSchema = Depends(get_current_user)):
    if user_updates.id and user.role == UserRole.USER and user_updates.id != user.id:
        raise HTTPException(status_code=403, detail='Forbidden')

    if user_updates.id is None:
        user_updates.id = user.id

    service = get_user_service(database)
    return await service.update_user(user_updates)


@router.delete('/delete')
async def delete_user(user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')

    service = get_user_service(database)
    return await service.delete_user(user_id if user_id else user.id)


@router.get('/my_books')
async def get_all_user_books(user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')

    service = get_shelf_service(database)
    return {'books': await service.get_all_shelf(user_id if user_id else user.id)}


@router.delete('/delete_book')
async def delete_book_from_library(book_id: int, user_id: int = None, user: UserSchema = Depends(get_current_user)):
    if user_id and user.role == UserRole.USER and user.id != user_id:
        raise HTTPException(status_code=403, detail='Forbidden')

    service = get_shelf_service(database)
    await service.delete_book_from_library(user_id if user_id else user.id, book_id)
    return {'detail': 'Book deleted from library'}
