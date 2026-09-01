from pydantic import BaseModel


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None


class Hotel(BaseModel):
    title: str
    location: str
