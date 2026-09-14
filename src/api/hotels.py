from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import (
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
)
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


# Метод Get, вернуть отели
@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Адрес"),
    date_from: date = Query(json_schema_extra={"example": "2026-09-04"}),
    date_to: date = Query(json_schema_extra={"example": "2026-09-06"}),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )


# Метод Get, вернуть один отель по его id
@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        hotel = await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return hotel


# метод Post, создание сущности
@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Первый вариант",
                "value": {"title": "Отель у моря", "location": "Сочи"},
            },
            "2": {
                "summary": "Второй вариант",
                "value": {"title": "Гостиница Центральная", "location": "Москва"},
            },
        }
    ),
):

    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"Status": "Ok", "data": hotel}


# Метод Put, Полностью заменить элементы сущности
@router.put("/{hotel_id}")
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).put_hotel(hotel_id, hotel_data)
    return {"Status": "Ok"}


# Метод Path, частично заменить элементы сущности
@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле",
)
async def partially_edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await HotelService(db).patch_hotel(hotel_id, hotel_data)
    return {"Status": "Ok"}


# Метод Delete, удалить сущность
@router.delete("/{hotel_id}")
async def delete_hostels(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"Status": "Ok"}
