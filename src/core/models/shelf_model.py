from sqlalchemy import Table, Column, Integer, Float, DateTime, ForeignKey, func
from src.db.database import metadata


bookshelf = Table(
    'bookshelf',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
    Column('book_id', Integer, ForeignKey('book.id', ondelete='CASCADE')),
    Column('bought_price', Float),
    Column('date_added', DateTime, server_default=func.now()),
    Column('last_time_read', DateTime, server_default=func.now())
)
