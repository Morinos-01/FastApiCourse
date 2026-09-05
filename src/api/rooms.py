from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAdd, RoomPatch, RoomPut, RoomAddRequest
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])




#Вернуть все номера по отелю
@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    pagination: PaginationDep
):
    per_page = pagination.per_page or 5
    return await db.rooms.get_all(
        limit=per_page,
        offset=per_page*(pagination.page-1),
        hotel_id=hotel_id
    )



#Вернуть конкретный номер
@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, room_id: int):
    room = await db.rooms.get_one_or_none(id=room_id)
    if not room:
        return {"status": "Такого номера нет"}
    return {"status": "ok", "room": room}


#Создать номер
@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
        "1": {
            "summary": "первый вариант",
            "value": {
                "title": "Одиночный",
                "description": "Номер с одной кроватью",
                "price": 1919,
                "qiantity": 18
            }
        },
        "2": {
            "summary": "второй вариант",
            "value": {
                "title": "Для новобрачных",
                "description": "С большой кроватью",
                "price": 3452,
                "qiantity": 32
            }
        }
    })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "Ok", "room": room}



#Удалить номер
@router.delete("/rooms/{room_id}")
async def delete_room(db: DBDep, room_id: int):
    await db.rooms.delete(id=room_id)
    await db.commit()
    return {"status": "Ok"}


#Полностью изменить номер
@router.put("/rooms/{room_id}")
async def put_room(db: DBDep, room_id: int,room_data: RoomPut):
    await db.rooms.edit(
        data=room_data,
        id=room_id
    )
    await db.commit()
    return {"status": "Ok"}


#Частично изменить номер
@router.patch("/rooms/{room_id}")
async def patch_room(db: DBDep, room_id: int, room_data: RoomPatch):
    await db.rooms.edit(
        data=room_data,
        exclude_unset=True,
        id=room_id
    )
    await db.commit()
    return {"status": "Ok"}