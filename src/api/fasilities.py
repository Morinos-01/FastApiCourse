from fastapi import APIRouter, Response

import json

from src.api.dependencies import DBDep
from src.schemas.fasilities import FasilitiesAdd
from src.init import redis_manager



router = APIRouter(prefix="/fasilities", tags=["Удобства"])


@router.get("")
async def get_fasilities(db: DBDep):
    fasilities_caсhe = await redis_manager.get("fasilities")
    if fasilities_caсhe:
        return Response(content=fasilities_caсhe, media_type="application/json")
    
    fasilities = await db.fasilities.get_all()
    _fasilities: list[dict] = [f.model_dump() for f in fasilities]
    fasilities_json = json.dumps(_fasilities)
    await redis_manager.set(key="fasilities", value=fasilities_json, expire=60)

    return fasilities   



@router.post("")
async def create_fasilitie(db: DBDep, fasilitie_data: FasilitiesAdd):
    fasilitie = await db.fasilities.add(fasilitie_data)
    await db.commit()
    return {"status": "Ok", "fasilitie": fasilitie}


