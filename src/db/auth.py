from src.db.database import database
from src.core.models.users_model import users
from src.schemas.user_schemas import UserInDBSchema


async def get_user(user_id: int) -> UserInDBSchema:
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query=query)
    return UserInDBSchema(**user) if user is not None else None


