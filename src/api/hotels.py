from fastapi import APIRouter, Body, Query

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelRepository
from src.schemas.hotels import Hotel, HotelPatch



router = APIRouter(prefix="/hotels", tags=["Отели", ])





# Метод Get, вернуть сущности
@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Адрес"),
    ):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page*(pagination.page-1)
        )



# метод Post, создание сущности
@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
            "1": {
                "summary": "Первый вариант",
                "value": {                  
                    "title": "Отель у моря",
                    "location": "Сочи"
                }
            },
            "2": {
                "summary": "Второй вариант",
                "value": {
                    "title": "Гостиница Центральная",
                    "location": "Москва"
                }
            }
        })
):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        await session.commit()

        return {"Status": "Ok", "data": hotel}


# Метод Delete, удалить сущность
@router.delete("/{hotel_id}")
def delete_hostels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"]!=hotel_id]
    return {"Status": "Ok"}



# Метод Put, Полностью заменить элементы сущности
@router.put("/{id_hotel}")
def put_hotel(id_hotel: int, hotel_data: Hotel):
    hotel = [hotel for hotel in hotels if hotel["id"] == id_hotel][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "ok"}






# Метод Path, частично заменить элементы сущности
@router.patch(
        "/{id_hotel}",
        summary="Частичное обновление данных об отеле",
        description="Тут мы частично обновляем данные об отеле"
           )
def path_hotel(
    id_hotel: int, 
    hotel_in: HotelPatch
    ):
    hotel = [hotel for hotel in hotels if hotel["id"] == id_hotel][0]
    if hotel_in.title is not None:
        hotel["title"] = hotel_in.title
    if hotel_in.name is not None:
        hotel["name"] = hotel_in.name
    return {"status": "good"}
