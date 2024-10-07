from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.db.database import database, create_tables
from contextlib import asynccontextmanager
import uvicorn
from src.endpoints import all_routers
from src.core.basic_admin import create_basic_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await create_tables()
    await create_basic_admin('admin@admin.com', 'admin')

    yield

    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(all_routers)



@app.get('/')
async def index_redirect():
    return RedirectResponse('/docs')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=3000, reload=True)
