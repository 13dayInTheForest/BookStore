from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.db.database import database, create_tables
from contextlib import asynccontextmanager
import uvicorn
from src.endpoints import all_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await create_tables()

    yield

    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(all_routers)


@app.get('/')
async def index_redirect():
    return RedirectResponse('/docs')


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
