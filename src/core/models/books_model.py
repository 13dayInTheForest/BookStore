from sqlalchemy import Table, Column, Integer, String, Float, DateTime, Enum, func
from src.db.database import metadata
from src.schemas.book_schemas import BookStatus


books = Table(
    'books',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(500), nullable=False),
    Column('author', String(256), nullable=False),
    Column('description', String(1000), nullable=True),
    Column('date_created', DateTime, nullable=False),
    Column('price', Float, default=0.0),
    Column('status', String, Enum(BookStatus).values_callable, default=BookStatus.DRAFT, nullable=False),
    Column('added_at', DateTime, server_default=func.now()),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
)


