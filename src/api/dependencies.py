from typing import Annotated
from pydantic import BaseModel
from fastapi import Query, Depends, Request, HTTPException

from src.services.auth import auth_service

class PaginationParams(BaseModel):
    page: Annotated [int | None, Query(1, gt=0)]
    per_page: Annotated [int | None,  Query(None, gt=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request)->str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token))->int:
    data = auth_service.decode_jwt(token)
    return data["user_id"]

UserIdDep = Annotated[int, Depends(get_current_user_id)]