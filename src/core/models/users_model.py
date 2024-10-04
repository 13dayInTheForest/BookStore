from sqlalchemy import Table, Column, Integer, String, Float, DateTime, func, Enum
from src.db.database import metadata
from src.schemas.user_schemas import UserRole

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('surname', String(50), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('password', String, nullable=False),
    Column('age', Integer, nullable=True),
    Column('balance', Float, default=0.0, nullable=False),
    Column('role', String, Enum(UserRole).values_callable, default=UserRole.USER, nullable=False),
    Column('register_at', DateTime, server_default=func.now())
)

