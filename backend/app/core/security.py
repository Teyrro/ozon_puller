from datetime import datetime, timedelta
from typing import Any

import jwt
from cryptography import fernet
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.base_schema import TokenType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fernet = fernet.Fernet(settings.SECRET_KEY.encode())


async def create_access_token(
    subject: str | Any,
    token_type: TokenType,
    expires_delta: timedelta = None,
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM,
    )


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


async def get_data_encrypt(data: str) -> str:
    data = fernet.encrypt(data.encode("utf-8"))
    return data.decode("utf-8")


async def get_context(variable: str) -> str:
    return fernet.decrypt(variable).decode()
