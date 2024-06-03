import logging

from sqlalchemy import AsyncAdaptedQueuePool, NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import ModeEnum, settings

logger = logging.getLogger(__name__)

engine = create_async_engine(
    str(settings.ASYNC_DATABASE_URI),
    echo=False,
    poolclass=NullPool
    if settings.MODE == ModeEnum.testing
    else AsyncAdaptedQueuePool,  # Asyncio pytest works with NullPool
    # pool_size=POOL_SIZE,
    # max_overflow=64,
)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

engine_celery = create_async_engine(
    str(settings.ASYNC_CELERY_BEAT_DATABASE_URI),
    echo=True,
    poolclass=NullPool
    if settings.MODE == ModeEnum.testing
    else AsyncAdaptedQueuePool,  # Asyncio pytest works with NullPool
    # pool_size=POOL_SIZE,
    # max_overflow=64,
)

SessionLocalCelery = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_celery,
    class_=AsyncSession,
    expire_on_commit=False,
)


