import asyncio
from collections.abc import AsyncGenerator, Coroutine
from typing import Any

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.core.init_db import init_db
from app.db.session import SessionLocal
from app.main import app
from app.schemas.role_schema import IRoleEnum
from app.tests.utils.user import authentication_token_from_email, create_random_user
from app.tests.utils.utils import get_superuser_token_headers

CLEAN_TABLES = [
    '"User"',
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        str(settings.ASYNC_DATABASE_URI), future=True, echo=True
    )
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    yield async_session()


@pytest.fixture(scope="function")
async def async_session_test():
    engine = create_async_engine(
        str(settings.ASYNC_DATABASE_URI), future=True, echo=True
    )
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    yield async_session()


@pytest.fixture(scope="function", autouse=True)
async def prepare_database(async_session_test):
    async with async_session_test as session:
        await init_db(session)
    yield
    async with async_session_test as session:
        for table_for_cleaning in CLEAN_TABLES:
            await session.execute(
                text(f""" TRUNCATE TABLE {table_for_cleaning} CASCADE;""")
            )
        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def client(async_session_test) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture
async def create_user(async_session_test):
    return await create_random_user(db=async_session_test())


@pytest_asyncio.fixture(scope="function")
async def superuser_token_headers(client: AsyncClient) -> dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest_asyncio.fixture(scope="function")
async def normal_user_token_headers(
    client: AsyncClient, async_session_test: SessionLocal
) -> Coroutine[Any, Any, dict[str, str]]:
    return await authentication_token_from_email(
        client=client,
        email=settings.EMAIL_TEST_USER,
        db=async_session_test,
        role=IRoleEnum.user,
    )
