from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import ShowUser, UserCreate
from app.core.security import get_password_hash
from app.db.crud import create_user, delete_user, get_user_by_id, update_user


async def _create_new_user(user: UserCreate, session: AsyncSession) -> ShowUser:
    async with session.begin():
        user = await create_user(
            name=user.name,
            surname=user.surname,
            email=user.email,
            hashed_password=get_password_hash(user.password),
            session=session,
        )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def _delete_new_user(user_id: UUID, session: AsyncSession) -> UUID | None:
    async with session.begin():
        deleted_user_id = await delete_user(user_id=user_id, session=session)
        return deleted_user_id


async def _update_user(
    updated_user_params: dict, user_id: UUID, session
) -> UUID | None:
    async with session.begin():
        updated_user_id = await update_user(
            user_id=user_id, session=session, **updated_user_params
        )
        return updated_user_id


async def _get_user_by_id(user_id: UUID, session: AsyncSession) -> ShowUser | None:
    async with session.begin():
        user = await get_user_by_id(user_id=user_id, session=session)
    if user is not None:
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )
