from sqlalchemy import select
from pydantic import BaseModel

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm



class HotelRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            title,
            location,
            limit,
            offset
    ):
        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.icontains(title))
        if location:
            query = query.filter(HotelsOrm.location.icontains(location))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        hotels = result.scalars().all()
        return hotels


    async def edit(
            self,
            data: BaseModel
    ):
        ...

    async def delete(
            self,
    ):
        ...