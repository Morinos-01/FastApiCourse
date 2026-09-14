import logging

from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AddOneObjectException, NotThisPasswordException, ObjectNotFoundException
from src.schemas.users import UserAdd, UserRequestAdd
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["Авторизация и аутентификация"])


# Регистрация пользователя
@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    hashed_password = auth_service.create_hashed_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add(new_user_data)
    except AddOneObjectException:
        raise HTTPException(status_code=409, detail="Такой пользователь уже имеется")

    await db.commit()
    return {"status": "ok"}


# Аутентификация пользователя
@router.post("/login")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    try:
        user = await db.users.get_user_with_hashed_password(email=data.email)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Неверный email или пароль")

    try:
        auth_service.verify_password(data.password, user.hashed_password)
    except NotThisPasswordException:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": "ok"}


# Получить данные аутентифицированного пользователя
@router.get("/get_me")
async def get_me(db: DBDep, user_id: UserIdDep):
    try:
        user = await db.users.get_one(id=user_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


# Разлогиниться
@router.delete("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "Ok"}
