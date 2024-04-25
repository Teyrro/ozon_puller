from collections.abc import Generator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import settings

engine = create_async_engine(
	settings.REAL_DATABASE_URL,
	future=True,
	echo=True,
	execution_options={'isolation_level': 'AUTOCOMMIT'},
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> Generator:
	"""dependency for getting async session"""
	try:
		session: AsyncSession = async_session()
		yield session
	finally:
		await session.close()
