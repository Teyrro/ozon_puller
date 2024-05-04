import enum
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import ShowUser, UserCreate
from app.core.security import get_password_hash
from app.db import crud
from app.db.models import PortalRole, User


class RequestAction(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


async def _create_new_user(user: UserCreate, session: AsyncSession) -> ShowUser:
    async with session.begin():
        user = await crud.create_user(
            name=user.name,
            surname=user.surname,
            email=user.email,
            hashed_password=get_password_hash(user.password),
            session=session,
            roles=[PortalRole.ROLE_PORTAL_USER],
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
        deleted_user_id = await crud.delete_user(user_id=user_id, session=session)
        return deleted_user_id


async def _update_user(
    updated_user_params: dict, user_id: UUID, session
) -> UUID | None:
    async with session.begin():
        updated_user_id = await crud.update_user(
            user_id=user_id, session=session, **updated_user_params
        )
        return updated_user_id


async def _get_user_by_id(user_id: UUID, session: AsyncSession) -> User | None:
    async with session.begin():
        user = await crud.get_user_by_id(user_id=user_id, session=session)
    if user is not None:
        return user


def check_user_permissions(
    target_user: User | None, current_user: User, action: RequestAction
) -> bool:
    if (
        PortalRole.ROLE_PORTAL_SUPERADMIN in current_user.roles
        and action == RequestAction.DELETE
    ):
        raise HTTPException(
            status_code=406, detail="Superadmin cannot be deleted via API."
        )
    if action == RequestAction.CREATE:
        if not {
            PortalRole.ROLE_PORTAL_ADMIN,
            PortalRole.ROLE_PORTAL_SUPERADMIN,
        }.intersection(current_user.roles):
            return False
    if (
        action in [RequestAction.UPDATE, RequestAction.DELETE]
        and target_user.user_id != current_user.user_id
    ):
        # check admin role
        if not {
            PortalRole.ROLE_PORTAL_ADMIN,
            PortalRole.ROLE_PORTAL_SUPERADMIN,
        }.intersection(current_user.roles):
            return False
        # check admin deactivate superadmin or admin attempt
        if {
            PortalRole.ROLE_PORTAL_SUPERADMIN,
            PortalRole.ROLE_PORTAL_ADMIN,
        }.intersection(
            target_user.roles
        ) and PortalRole.ROLE_PORTAL_ADMIN in current_user.roles:
            return False
    return True
