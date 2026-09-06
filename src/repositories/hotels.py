from datetime import date
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.models.rooms import RoomsOrm



class HotelRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel


#Получить список отелей со свободными номерами
    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            title,
            location,
            limit,
            offset
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = (
            select(HotelsOrm)
            .filter(HotelsOrm.id.in_(hotels_ids_to_get))
        )
        if title:
            query = query.filter(HotelsOrm.title.icontains(title))
        if location:
            query = query.filter(HotelsOrm.location.icontains(location))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        hotels = result.scalars().all()
        return [self.schema.model_validate(model, from_attributes=True) for model in hotels]

