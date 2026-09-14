from pydantic import BaseModel

from datetime import date

from src.services.base import BaseService
from src.services.hotels import HotelService
from src.schemas.fasilities import RoomsFasilitiesAdd
from src.schemas.rooms import RoomAdd, RoomPatch, Room
from src.exceptions import ObjectNotFoundException, HotelNotFoundException, RoomNotFoundException


class RoomService(BaseService):
    # Вернуть все номера
    async def get_filtered(
        self,
        hotel_id: int,
    ):
        return await self.db.rooms.get_filtered(hotel_id=hotel_id)

    # Вернуть один номер
    async def get_room(
        self,
        room_id: int,
    ):
        room = await self.db.rooms.get_one_with_rels(id=room_id)
        return room

    # Вернуть, доступные на определенные даты, номера по определенному отелю
    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,

    ):
        return await self.db.rooms.get_filtered_by_time(hotel_id, date_from=date_from, date_to=date_to)

    # Создать номер
    async def add_room(
        self,
        hotel_id: int,
        room_data: BaseModel
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
    
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        
        room = await self.db.rooms.add(_room_data)
    
        room_fasilities_data = [
            RoomsFasilitiesAdd(room_id=room.id, fasilitie_id=f_id) for f_id in room_data.facilities_ids
        ]
        await self.db.rooms_fasilities.add_bulk(room_fasilities_data)
    
        await self.db.commit()

    # Изменить номер
    async def put_room(self, hotel_id: int, room_id: int, room_data: BaseModel):
        await HotelService(self.db).get_hotel_and_check(hotel_id)
        await self.get_room_and_check(room_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(data=_room_data, id=room_id)
        await self.db.rooms_fasilities.set_room_fasilities(
            room_id=room_id, fasilities_ids=room_data.facilities_ids
        )
        await self.db.commit()

    # Частично изменить номер
    async def patch_room(self,hotel_id: int, room_id: int, room_data: BaseModel):
        await HotelService(self.db).get_hotel_and_check(hotel_id)
        await self.get_room_and_check(room_id)

        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id)
        if "fasilities_ids" in _room_data_dict:
            await self.db.rooms_fasilities.set_room_fasilities(
                room_id=room_id, fasilities_ids=_room_data_dict["fasilities_ids"]
            )
        await self.db.commit()

    # Удалить номер
    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_and_check(hotel_id)
        await self.get_room_and_check(room_id)

        await self.db.rooms.delete(id=room_id)
        await self.db.commit()

    # Получить номер
    async def get_room_and_check(self, room_id)->Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
