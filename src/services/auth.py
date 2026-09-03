
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import HTTPException
import jwt

from src.config import settings


class AuthService:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= ({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt


    def create_hashed_password(self, password):
        return self.pwd_context.hash(password)


    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)


    def decode_jwt(self, token: str)->dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="Неверный токен")

auth_service = AuthService()