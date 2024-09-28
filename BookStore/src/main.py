from fastapi import FastAPI
from src.db.database import database, create_tables
from contextlib import asynccontextmanager
import uvicorn
from src.endpoints.user_endpoint import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await create_tables()

    yield

    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=3000, reload=True)
