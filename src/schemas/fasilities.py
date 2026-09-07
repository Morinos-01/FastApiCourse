from pydantic import BaseModel


#Схемы для сущности "Fasilities"
class FasilitiesAdd(BaseModel):
    title: str


class Fasilities(FasilitiesAdd):
    id: int

class FasilitiesPath(BaseModel):
    title: str | None = None




#Схемы для вспомогательной таблицы RoomsFasilities
class RoomsFasilitiesAdd(BaseModel):
    room_id: int
    fasilitie_id: int


class RoomsFasilities(RoomsFasilitiesAdd):
    id: int