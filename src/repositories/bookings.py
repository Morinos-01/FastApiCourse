from sqlalchemy import select, insert
from fastapi import HTTPException

from datetime import date
from pydantic import BaseModel

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingsDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsOrm
from src.schemas.bookings import BookingAddRequest




class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingsDataMapper

    async def get_bookings_with_today_checking(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking_data: BookingAddRequest):
        available_rooms_query = rooms_ids_for_booking(
        date_to=booking_data.date_to,
        date_from=booking_data.date_from,
    )
        room_query = (
            select(RoomsOrm)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(available_rooms_query))
            .filter_by(id=booking_data.room_id)
        )
        room_res = await self.session.execute(room_query)
        room = room_res.scalars().one_or_none()
        print(room)
        if room is None:
            raise HTTPException(status_code=422, detail="К сожалению, на выбранные даты нет свободных номеров.")

        booking_add_stmt = (
            insert(self.model)
            .values(**booking_data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(booking_add_stmt)
        model = result.scalar_one()
        return self.mapper.map_to_domain_entity(model)
        