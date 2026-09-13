from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])



#создать бронь
@router.post("")
async def create_bookings(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    booking = await db.bookings.add_booking(booking_data=_booking_data)
    await db.commit()
    return {"status": "ok", "booking": booking}


#получить все брони без авторизации
@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


#Получить брони авторизированного пользователя
@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)
