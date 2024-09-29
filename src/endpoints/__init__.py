from fastapi import APIRouter
from .user_endpoint import router as user_router
from .book_endpoint import router as book_router


all_routers = APIRouter()

all_routers.include_router(user_router, tags=['user'])
all_routers.include_router(book_router, tags=['books'])
