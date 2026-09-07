from src.repositories.mappers.base import DataMapper
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking





class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel




class BookingsDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking

