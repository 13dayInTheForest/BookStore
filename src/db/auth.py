from src.db.database import database
from src.core.models.users_model import users
from src.schemas.user_schemas import UserInDBSchema


async def get_user(email: str) -> UserInDBSchema | None:
    query = users.select().where(users.c.email == email)
    user = await database.fetch_one(query=query)
    return UserInDBSchema(**user) if user is not None else None


