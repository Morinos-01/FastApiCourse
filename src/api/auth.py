from fastapi import APIRouter, HTTPException, Response, Request

from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.repositories.users import UsersRepository
from src.services.auth import auth_service
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/users", tags=["Авторизация и аутентификация"])



@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = auth_service.create_hashed_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

        return {"status": "good"}



@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not auth_service.verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        
        access_token = auth_service.create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": "ok"}



@router.get("/get_me")
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user


@router.delete("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "Ok"}