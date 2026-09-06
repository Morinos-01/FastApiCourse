from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

#Получить свободные номера в эти даты
    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from,
            date_to
    ):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        # print(query.compile(
        #     dialect=self.session.bind.dialect,
        #     compile_kwargs={"literal_binds": True})
        # )

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))