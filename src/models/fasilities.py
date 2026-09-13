from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.rooms import RoomsOrm

class FasilitiesOrm(Base):
    __tablename__ = "fasilities"

    id: Mapped[int] = mapped_column(primary_key=True) 
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="fasilities",
        secondary="rooms_fasilities"
    )



class RoomsFasilitiesOrm(Base):
    __tablename__ = "rooms_fasilities"

    id: Mapped[int] = mapped_column(primary_key=True) 
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    fasilitie_id: Mapped[int] = mapped_column(ForeignKey("fasilities.id"))


