from pydantic import BaseModel


class HotelPut(BaseModel):
    title: str | None = None
    name: str | None = None


class Hotel(BaseModel):
    title: str
    name: str