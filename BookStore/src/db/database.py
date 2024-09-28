import sqlalchemy.dialects.postgresql
from sqlalchemy.ext.asyncio import create_async_engine
from databases import Database
from sqlalchemy import MetaData
from src.core.config import settings


database = Database(settings.get_db_url)
engine = create_async_engine(settings.get_db_url)
metadata = MetaData()
dialect = sqlalchemy.dialects.postgresql.dialect()


async def create_tables():
    async with engine.connect() as connect:
        await connect.run_sync(metadata.create_all)
        await connect.commit()


async def drop_tables():
    async with engine.connect() as connect:
        await connect.run_sync(metadata.drop_all)
        await connect.commit()
