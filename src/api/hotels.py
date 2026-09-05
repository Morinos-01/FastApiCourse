from fastapi import APIRouter, Body, Query

from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelAdd, HotelPatch
from src.api.dependencies import DBDep



router = APIRouter(prefix="/hotels", tags=["Отели"])





# Метод Get, вернуть отели
@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Адрес"),
    ):
    per_page = pagination.per_page or 5

    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=per_page*(pagination.page-1)
    )


# Метод Get, вернуть один отель по его id
@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)



# метод Post, создание сущности
@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"Status": "Ok", "data": hotel}


# Метод Delete, удалить сущность
@router.delete("/{hotel_id}")
async def delete_hostels(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"Status": "Ok"}




# Метод Put, Полностью заменить элементы сущности
@router.put("/{hotel_id}")
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "ok"}




# Метод Path, частично заменить элементы сущности
@router.patch(
        "/{hotel_id}",
        summary="Частичное обновление данных об отеле",
        description="Тут мы частично обновляем данные об отеле"
           )
async def partially_edit_hotel(
    db: DBDep,
    hotel_id: int, 
    hotel_data: HotelPatch
    ):

    await db.hotels.edit(
        data=hotel_data,
        exclude_unset=True,
        id=hotel_id
    )
    await db.commit()
    return {"status": "good"}