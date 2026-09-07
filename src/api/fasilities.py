from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.fasilities import FasilitiesAdd


router = APIRouter(prefix="/fasilities", tags=["Удобства"])


@router.get("")
async def get_fasilities(db: DBDep):
    return await db.fasilities.get_all()


@router.post("")
async def create_fasilitie(db: DBDep, fasilitie_data: FasilitiesAdd):
    fasilitie = await db.fasilities.add(fasilitie_data)
    await db.commit()
    return {"status": "Ok", "fasilitie": fasilitie}


