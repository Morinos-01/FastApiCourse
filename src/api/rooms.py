from fastapi import APIRouter, Body, Query
from datetime import date

from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.schemas.fasilities import RoomsFasilitiesAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])




#Вернуть все номера по отелю
@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
):
    return await db.rooms.get_filtered(
        hotel_id=hotel_id
    )



#Вернуть, доступные на определенные даты, номера по определенному отелю
@router.get("/{hotel_id}/available_rooms")
async def get_available_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(json_schema_extra={"example": "2026-09-04"}),
    date_to: date = Query(json_schema_extra={"example": "2026-09-06"}),
):
    return await db.rooms.get_filtered_by_time(hotel_id, date_from=date_from, date_to=date_to)



#Вернуть конкретный номер
@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, room_id: int):
    room = await db.rooms.get_one_or_none_with_rels(id=room_id)
    if not room:
        return {"status": "Такого номера нет"}
    return {"status": "ok", "room": room}


#Создать номер
@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep, 
    hotel_id: int, 
    room_data: RoomAddRequest = Body(openapi_examples={
        "1": {
            "summary": "первый вариант",
            "value": {
                "title": "Одиночный",
                "description": "Номер с одной кроватью",
                "price": 1919,
                "qiantity": 18,
                "facilities_ids": [1, 2, 3]
            }
        },
        "2": {
            "summary": "второй вариант",
            "value": {
                "title": "Для новобрачных",
                "description": "С большой кроватью",
                "price": 3452,
                "qiantity": 32,
                "facilities_ids": [4, 5]
            }
        }
    })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    room_fasilities_data = [RoomsFasilitiesAdd(room_id=room.id, fasilitie_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_fasilities.add_bulk(room_fasilities_data)

    await db.commit()
    return {"status": "Ok", "room": room}



#Удалить номер
@router.delete("/rooms/{room_id}")
async def delete_room(db: DBDep, room_id: int):
    await db.rooms.delete(id=room_id)
    await db.commit()
    return {"status": "Ok"}


#Полностью изменить номер
@router.put("{hotel_id}/rooms/{room_id}")
async def put_room(db: DBDep, room_id: int, hotel_id: int,room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(
        data=_room_data,
        id=room_id
    )
    await db.rooms_fasilities.set_room_fasilities(room_id=room_id, fasilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "Ok"}


#Частично изменить номер
@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(db: DBDep, room_id: int, hotel_id: int, room_data: RoomPatchRequest):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(
        data=_room_data,
        exclude_unset=True,
        id=room_id
    )
    if "fasilities_ids" in _room_data_dict:
        print("говно----------------", _room_data_dict["fasilities_ids"])
        await db.rooms_fasilities.set_room_fasilities(room_id=room_id, fasilities_ids=_room_data_dict["fasilities_ids"])
    await db.commit()
    return {"status": "Ok"}