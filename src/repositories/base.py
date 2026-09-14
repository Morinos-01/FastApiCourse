from collections.abc import Sequence
import logging

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.exceptions import AddOneObjectException, ObjectNotFoundException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    # Получить всё
    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(data=model) for model in result.scalars().all()]

    # Получить с фильтром
    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    # Получить одну единицу или None
    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(model)

    # Создать Сущность
    async def add(
        self,
        data: BaseModel,
    ):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_stmt)
        except IntegrityError as ex:
            logging.error(
                f"Не удалось добавить данные в бд, входные данные date={data}, тип ошибки: {type(ex.orig.__cause__)}"
                )
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise AddOneObjectException from ex
            else:
                logging.error(
                    f"Незнакомая ошибка: не удалось добавить данные в бд, входные данные date={data}, тип ошибки тип ошибки: {type(ex.orig.__cause__)}"
                    )
                raise ex

        model = result.scalar_one()
        return self.mapper.map_to_domain_entity(model)

    # Создать несколько сущностей
    async def add_bulk(self, data: Sequence[BaseModel]):
        add_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_stmt)

    # Изменить Сущность
    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    # Удалить Сущность
    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
