import asyncio
from typing import Any, Callable, Generator, Union

import pytest
from sqlalchemy import NullPool, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from starlette.testclient import TestClient

import settings
from db.models import User
from db.session import get_db
from main import app

# create async engine for interaction with database
test_engine = create_async_engine(
    settings.TEST_DATABASE_URL, future=True, echo=True, poolclass=NullPool
)

# create session for the interaction with database
test_async_session = async_sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)

CLEAN_TABLES = [
    "users",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    pass
    # os.system("alembic init --template async test_migrations")
    # os.system('alembic revision --autogenerate -m "test running migrations"')
    # os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session, session.begin():
        for table_for_cleaning in CLEAN_TABLES:
            await session.execute(text(f""" TRUNCATE TABLE {table_for_cleaning};"""))


async def _get_test_db():
    try:
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
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
async def create_user_in_database(async_session_test) -> Union[Callable, None]:
    async def create_user_in_database(user: dict):
        new_user = User(
            name=user["name"],
            surname=user["surname"],
            email=user["email"],
            is_active=user["is_active"],
        )
        async with async_session_test() as session:
            session.add(new_user)
            await session.commit()
            return new_user.user_id

    return create_user_in_database
