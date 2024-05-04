from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import PortalRole, User


async def create_user(
    name: str,
    surname: str,
    email: str,
    hashed_password: str,
    roles: list[PortalRole],
    session: AsyncSession,
) -> User:
    new_user = User(
        name=name,
        surname=surname,
        email=email,
        hashed_password=hashed_password,
        roles=roles,
    )
    session.add(new_user)
    await session.flush()
    return new_user


async def delete_user(user_id: UUID, session: AsyncSession) -> UUID | None:
    query = (
        update(User)
        .where(and_(User.user_id == user_id, User.is_active == True))
        .values(is_active=False)
        .returning(User.user_id)
    )
    res = await session.execute(query)
    deleted_user_id_row = res.fetchone()
    if deleted_user_id_row is not None:
        return deleted_user_id_row[0]


async def get_user_by_id(user_id: UUID, session: AsyncSession) -> User | None:
    query = select(User).where(User.user_id == user_id)
    res = await session.execute(query)
    user_row = res.fetchone()
    if user_row is not None:
        return user_row[0]


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    query = select(User).where(User.email == email)
    res = await session.execute(query)
    user_row = res.fetchone()
    if user_row is not None:
        return user_row[0]


async def update_user(user_id: UUID, session: AsyncSession, **kwargs) -> UUID | None:
    query = (
        update(User)
        .where(and_(User.user_id == user_id, User.is_active == True))
        .values(kwargs)
        .returning(User.user_id)
    )
    res = await session.execute(query)
    update_user_id_row = res.fetchone()
    if update_user_id_row is not None:
        return update_user_id_row[0]
