from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    # Получить свободные номера в эти даты
    async def get_filtered_by_time(self, hotel_id, date_from, date_to):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.fasilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRels.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]

    # Получить один номер
    async def get_one_with_rels(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.fasilities)).filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise RoomNotFoundException

        return RoomWithRels.model_validate(model, from_attributes=True)
