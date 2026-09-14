from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Нет свободных номеров"


class AddOneObjectException(NabronirovalException):
    detail = "Не получилось добавить сущность"


class NotThisPasswordException(NabronirovalException):
    detail = "Пароль не верный"


def check_date_to_after_date_from(date_from: date, date_to: date):
    if date_from >= date_to:
        raise HTTPException(status_code=400, detail="Дата заезда позже или равна даты выезда")


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"
