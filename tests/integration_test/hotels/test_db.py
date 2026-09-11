from src.schemas.hotels import HotelAdd

async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Калифорния", location="Где то в Калифорнии")
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    
    print(hotel)