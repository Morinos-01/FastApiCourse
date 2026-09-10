from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager


import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.auth import router as router_users
from src.api.bookings import router as router_bookings
from src.api.fasilities import router as router_fasilities
from src.api.images import router as router_images


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.disconnect()


app = FastAPI(lifespan=lifespan) 


app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_fasilities)
app.include_router(router_bookings)
app.include_router(router_images)




if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)    