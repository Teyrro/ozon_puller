from datetime import datetime, timedelta
from typing import Any

import fernet
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fernet = fernet.Fernet(settings.SECRET_KEY.encode())


def create_access_token(
        subject: EmailStr | Any, expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM,
    )


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_data_encrypt(data) -> str:
    data = fernet.encrypt(data)
    return data.decode("utf-8")


def get_context(variable: str) -> str:
    return fernet.decrypt(variable.encode()).decode()
