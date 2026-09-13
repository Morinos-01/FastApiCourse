from sqlalchemy import delete, insert, select

from src.models.fasilities import FasilitiesOrm, RoomsFasilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    FasilitiesDataMapper,
    RoomsFasilitiesDataMapper,
)


#Репозиторий для таблицы Fasilities
class FasilitiesRepository(BaseRepository):
    model = FasilitiesOrm
    mapper = FasilitiesDataMapper



#Репозиторий для вспомогательной таблицы
class RoomsFasilities(BaseRepository):
    model = RoomsFasilitiesOrm
    mapper = RoomsFasilitiesDataMapper


    #Добавить связь Rooms и Fasilities в вспомогательную таблицу
    async def set_room_fasilities(self, room_id: int, fasilities_ids: list[int]):
        query = (
            select(self.model.fasilitie_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(query)
        current_fasilities : list[list] = res.scalars().all()

        to_add: list[int] = list(set(fasilities_ids) - set(current_fasilities))
        to_delete: list[int] = list(set(current_fasilities) - set(fasilities_ids))

        if to_delete:
            stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.fasilitie_id.in_(to_delete)
                )
            )
            await self.session.execute(stmt)

        if to_add:
            stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "fasilitie_id": f_id} for f_id in to_add])
            )
            await self.session.execute(stmt)