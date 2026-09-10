from src.repositories.mappers.base import DataMapper
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking
from src.models.fasilities import FasilitiesOrm, RoomsFasilitiesOrm
from src.schemas.fasilities import Fasilities, RoomsFasilities
from src.models.users import UsersOrm
from src.schemas.users import User
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room




class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel




class BookingsDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking



class FasilitiesDataMapper(DataMapper):
    db_model = FasilitiesOrm
    schema = Fasilities



class RoomsFasilitiesDataMapper(DataMapper):
    db_model = RoomsFasilitiesOrm
    schema = RoomsFasilities


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room
