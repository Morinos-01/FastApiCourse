from typing import Annotated
from pydantic import BaseModel
from fastapi import Query, Depends

class PaginationParams(BaseModel):
    page: Annotated [int | None, Query(1, gt=0)]
    per_page: Annotated [int | None,  Query(None, gt=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]