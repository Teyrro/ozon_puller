from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, Path, status

from app import crud
from app.models import User
from app.models.role_model import Role
from app.schemas.user_schema import IUserCreate, IUserRead
from app.utils.exceptions.common_exceptions import IdNotFoundException


async def user_exists(new_user: IUserCreate) -> IUserCreate:
    user = await crud.user.get_by_email(email=new_user.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a user with same email",
        )
    role = await crud.role.get(id=new_user.role_id)
    if not role:
        raise IdNotFoundException(Role, id=new_user.role_id)

    return new_user


async def is_valid_user(
    user_id: Annotated[UUID, Path(title="The UUID id of the user")],
) -> IUserRead:
    user = await crud.user.get(id=user_id)
    if not user:
        raise IdNotFoundException(User, id=user_id)

    return user


async def is_valid_user_id(
    user_id: Annotated[UUID, Path(title="The UUID id of the user")],
) -> UUID:
    user = await crud.user.get(id=user_id)
    if not user:
        raise IdNotFoundException(User, id=user_id)

    return user_id
