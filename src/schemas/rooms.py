from pydantic import BaseModel


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



class RoomPut(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int 
    qiantity: int


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    qiantity: int | None = None