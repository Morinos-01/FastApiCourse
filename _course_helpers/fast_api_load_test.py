import time
import asyncio
import uvicorn
from fastapi import FastAPI


app = FastAPI(docs_url=None)


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Начал {id}: {time. time(): 2f}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time. time(): .2f}")



@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Начал {id}: {time. time(): 2f}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time. time(): .2f}")


if __name__ == "__main__":
    uvicorn.run(app="fast_api_load_test:app", reload=True)