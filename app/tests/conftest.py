import asyncio
import os
from collections.abc import Callable, Generator
from datetime import timedelta
from typing import Any

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from starlette.testclient import TestClient


from app.core.config import settings
from app.core.security import get_password_hash, create_access_token
from app.db.models import User
from app.db.session import get_db
from main import app

CLEAN_TABLES = [
    'users',
]


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def run_migrations():
    pass
    os.system('alembic init --template async test_migrations')
    os.system('alembic revision --autogenerate -m "tests running migrations"')
    os.system('alembic upgrade heads')


@pytest.fixture(scope='session')
async def async_session_test():
    engine = create_async_engine(str(settings.TEST_SQLALCHEMY_DATABASE_URI), future=True, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope='function', autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running tests function"""
    async with async_session_test() as session, session.begin():
        for table_for_cleaning in CLEAN_TABLES:
            await session.execute(text(f""" TRUNCATE TABLE {table_for_cleaning};"""))


async def _get_test_db():
    try:
        test_engine = create_async_engine(str(settings.TEST_SQLALCHEMY_DATABASE_URI), future=True, echo=True)
        test_async_session = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope='function')
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def get_user_from_database(async_session_test):
    async def get_user_from_database_by_uuid(user_id: str) -> User:
        async with async_session_test() as session:
            return await session.scalar(select(User).where(User.user_id == user_id))

    return get_user_from_database_by_uuid


@pytest.fixture
async def create_user_in_database(async_session_test) -> Callable:
    async def create_user_in_database(user: dict):
        new_user = User(
            name=user['name'],
            surname=user['surname'],
            email=user['email'],
            is_active=user['is_active'],
            hashed_password=get_password_hash(user['password']),
        )
        async with async_session_test() as session:
            session.add(new_user)
            await session.commit()
            return new_user.user_id

    return create_user_in_database


def create_test_auth_for_user(email: str) -> dict[str, str]:
    access_token = create_access_token(
       data={"sub": email},
       expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"Authorization": f"Bearer {access_token}"}
