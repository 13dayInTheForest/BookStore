from fastapi import APIRouter, Depends
from src.schemas.user_schemas import CreateUserSchema



router = APIRouter(
    prefix='/auth'
)


@router.get('/token')
async def get_jwt_token(user):




@router.get('/refresh')