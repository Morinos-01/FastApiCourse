from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    AllRoomsAreBookedException,
    ObjectNotFoundException,
    check_date_to_after_date_from,
)
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


# создать бронь
@router.post("")
async def create_bookings(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    check_date_to_after_date_from(booking_data.date_from, booking_data.date_to)

    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найдне")

    room_price = room.price
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())

    try:
        booking = await db.bookings.add_booking(booking_data=_booking_data)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    await db.commit()
    return {"status": "ok", "booking": booking}


# получить все брони без авторизации
@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


# Получить брони авторизированного пользователя
@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)
