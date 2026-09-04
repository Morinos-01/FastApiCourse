from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
            self, 
            limit, 
            offset,
            **filter_by
    ):
        query = select(self.model).filter_by(**filter_by).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]