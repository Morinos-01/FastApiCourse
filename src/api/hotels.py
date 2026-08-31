from fastapi import Query, APIRouter
from src.schemas.hotels import *
from src.api.dependencies import PaginationDep


router = APIRouter(prefix="/hotels", tags=["Отели", ])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": 'dubai'},
    {"id": 3, "title": "Мальдивы", "name": 'maldivi'},
    {"id": 4, "title": "Гелледжик", "name": 'gelendjik'},
    {"id": 5, "title": "Ханой", "name": 'hanoi'},
    {"id": 6, "title": "Дананг", "name": 'danang'},
    {"id": 7, "title": "Москва", "name": 'moskva'},
    {"id": 8, "title": "Майами", "name": 'maiami'},
    {"id": 9, "title": "Токио", "name": 'tokio'},
    {"id": 10, "title": "Гонконг", "name": 'gonkong'},
    
]



# Метод Get, вернуть сущности
@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(default=None, description="Айдишник"),
    title: str | None = Query(default=None, description="Название отеля"),
    ):

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    
    return hotels_[pagination.per_page*(pagination.page-1):][:pagination.per_page]


# метод Post, создание сущности
@router.post("")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({ 
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
        })
    return {"Status": "Ok"}


# Метод Delete, удалить сущность
@router.delete("/{hotel_id}")
def delete_hostels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"]!=hotel_id]
    return {"Status": "Ok"}



# Метод Put, Полностью заменить элементы сущности
@router.put("/{id_hotel}")
def put_hotel(id_hotel: int, hotel_data: Hotel):
    hotel = [hotel for hotel in hotels if hotel["id"] == id_hotel][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "ok"}






# Метод Path, частично заменить элементы сущности
@router.patch(
        "/{id_hotel}",
        summary="Частичное обновление данных об отеле",
        description="Тут мы частично обновляем данные об отеле"
           )
def path_hotel(
    id_hotel: int, 
    hotel_in: HotelPut
    ):
    hotel = [hotel for hotel in hotels if hotel["id"] == id_hotel][0]
    if hotel_in.title is not None:
        hotel["title"] = hotel_in.title
    if hotel_in.name is not None:
        hotel["name"] = hotel_in.name
    return {"status": "good"}
