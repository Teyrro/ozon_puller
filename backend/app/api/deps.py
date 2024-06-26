from collections.abc import AsyncGenerator, Callable, Coroutine
from contextlib import asynccontextmanager
from typing import Annotated, Any

import aioredis
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, MissingRequiredClaimError
from multipart.exceptions import DecodeError
from redis.asyncio import Redis
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app import crud
from app.core.config import settings
from app.core.security import decode_token
from app.db.session import SessionLocal, SessionLocalCelery
from app.models.user_models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_redis_client() -> Redis:
    redis = await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_NUMBER}",
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_jobs_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocalCelery() as session:
        yield session


async def check_auth(token: str) -> Any:
    try:
        payload = await decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your token has expired. Please log in again.",
        )
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Error when decoding the token. Please check your request.",
        )
    except MissingRequiredClaimError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="There is no required field in your token. Please contact the administrator.",
        )
    return payload


def get_current_user(
    required_roles: list[str] = None,
) -> Callable[[str], Coroutine[Any, Any, User]]:
    async def current_user(
        access_token: TokenDep,
    ) -> User:
        payload = await check_auth(access_token)
        user_id = payload["sub"]
        user: User = await crud.user.get(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        if required_roles:
            is_valid_role = False
            for role in required_roles:
                if role == user.role.name:
                    is_valid_role = True

            if not is_valid_role:
                raise HTTPException(
                    status_code=403,
                    detail=f"""Role "{required_roles}" is required for this action""",
                )

        return user

    return current_user


UserAuthDep = Annotated[User, Depends(get_current_user())]
