import json
from collections.abc import AsyncGenerator
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, async_session_maker_null_pool, engine_null_pool
from src.main import app
from src.models.__init__ import *
from src.schemas.fasilities import FasilitiesAdd
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager

"""
Этот файл запускается одним из первых, когда мы запускаем тесты
"""


#Подмена функции get_db в app
async def get_db_null_pool() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool


#создание объекта подклдючения к бд
@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


#создания объекта отправки запросов
@pytest.fixture(scope="session")
async def ac()->AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac




#Проверка, что мы работаем с env-test
@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"




#Снести и создать таблицы 
@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)




    #Вставить данные в бд
@pytest.fixture(scope="session", autouse=True)
async def add_data_in_database(setup_database):
    base_dir = Path(__file__).parent
    hotels_file = base_dir / "mock_hotels.json"
    rooms_file = base_dir / "mock_rooms.json"
    fasilities_file = base_dir / "mock_fasilities.json"

    with open(hotels_file, "r", encoding="utf-8") as file: #noqa: ASYNC230
        dict_hotels = json.load(file)

    with open(rooms_file, "r", encoding="utf-8") as file: #noqa: ASYNC230
        dict_rooms = json.load(file)

    with open(fasilities_file, "r", encoding="utf-8") as file: #noqa: ASYNC230
        dict_fasilities = json.load(file)

    data_hotels :list[HotelAdd] = [HotelAdd.model_validate(hotel) for hotel in dict_hotels]
    data_rooms :list[RoomAdd] = [RoomAdd.model_validate(room) for room in dict_rooms]
    data_fasilities :list[FasilitiesAdd] = [FasilitiesAdd.model_validate(fasilitie) for fasilitie in dict_fasilities]
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(data_hotels)
        await db.rooms.add_bulk(data_rooms)
        await db.fasilities.add_bulk(data_fasilities)
        await db.commit()





#запрос на создание пользователя
@pytest.fixture(scope="session", autouse=True)
async def register_user(add_data_in_database, ac):
    await ac.post(
        url="/users/register",
        json={
            "email": "user@e324xample.com", 
            "password": "string"
        },
    )


#Запрос на аутентификацию пользователя
@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    await ac.post(
        url="/users/login",
        json={
            "email": "user@e324xample.com", 
            "password": "string"
        },
    )
    assert ac.cookies["access_token"]
    yield ac




    

#Мок для запросов в Redis
@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    monkeypatch.setattr(
        "src.connectors.redis_connector.RedisManager.set",
        AsyncMock(return_value=None)
    )
    monkeypatch.setattr(
        "src.connectors.redis_connector.RedisManager.get",
        AsyncMock(return_value=None)
    )