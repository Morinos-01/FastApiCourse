from datetime import date

import pytest

from src.exceptions import ObjectNotFoundException
from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    # Делаем post запрос, создаем строчку в бд, booking
    user = (await db.users.get_all())[0].id
    room = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user,
        room_id=room,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    # read/getЗапрос - проверяем его и заодно create/postЗапрос
    booking = await db.bookings.get_one(id=new_booking.id)
    assert booking
    assert booking == new_booking

    # обновить бронь - проверка
    update_date = date(year=2024, month=8, day=25)
    update_booking_data = BookingAdd(
        user_id=user,
        room_id=room,
        date_from=date(year=2024, month=8, day=10),
        date_to=update_date,
        price=100,
    )
    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == update_date

    # Удалить бронь, проверка
    await db.bookings.delete(id=new_booking.id)
    with pytest.raises(ObjectNotFoundException):
        await db.bookings.get_one(id=new_booking.id)

    await db.rollback()
