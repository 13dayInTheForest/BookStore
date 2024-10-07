from src.db.repositories.user_repository import UserRepository
from src.db.database import database
from src.core.models.users_model import users
from src.schemas.user_schemas import UserSchema, CreateUserWithRole
from src.core.security import get_password_hash


async def create_basic_admin(email, password):
    user_repo = UserRepository(database, users, UserSchema)
    if not await user_repo.email_check_up(email):
        password = get_password_hash(password)
        admin = CreateUserWithRole(
            name='admin',
            surname='admin',
            email=email,
            password=password,
            age=None,
            balance=0.0,
            role='admin'
        )
        await user_repo.create(admin)

