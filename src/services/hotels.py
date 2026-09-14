from datetime import date
from pydantic import BaseModel

from src.services.base import BaseService
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import Hotel


class HotelService(BaseService):
    # Получить все отели
    async def get_filtered_by_time(
            self,
            pagination,
            title: str | None,
            location: str | None,
            date_from: date,
            date_to: date,
        ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        
        return await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )

    # Получить один отель
    async def get_hotel(self, hotel_id: int):
        hotel = await self.db.hotels.get_one(id=hotel_id)
        return hotel

    # Добавить отель
    async def add_hotel(self, hotel_data: BaseModel):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    # Заменить данные отеля
    async def put_hotel(self, hotel_id: int, hotel_data: BaseModel):
        await self.db.hotels.edit(data=hotel_data, id=hotel_id)
        await self.db.commit()

    # Частично заменить данные отеля
    async def patch_hotel(self, hotel_id: int, hotel_data: BaseModel):
        await self.db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    # Удалить отель
    async def delete_hotel(self, hotel_id):
        await self.db.hotels.delete(id=hotel_id)

    # Вернуть один отель
    async def get_hotel_and_check(self, hotel_id)->Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
