from pydantic import BaseModel

from src.schemas.fasilities import Fasilities


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    qiantity: int

class Room(RoomAdd):
    id: int



class RoomAddRequest(BaseModel):
    title: str
    description: str | None
    price: int
    qiantity: int
    facilities_ids: list[int] = []



class RoomWithRels(Room):
    fasilities: list[Fasilities]




class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    qiantity: int | None = None
    fasilities_ids: list[int] = []
    

class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    qiantity: int | None = None