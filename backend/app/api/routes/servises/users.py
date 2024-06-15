import enum
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import and_, col, or_, select
from starlette import status

from app.core.security import get_password_hash
from app.crud.user_crud import CRUDUser
from app.models import Role
from app.models.user_models import User
from app.schemas.user_schema import (
    IUserCreate,
    IUserStatus,
    IUserUpdate,
    IUserUpdateMe,
    IUserUpdatePassword,
)


class RequestAction(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class UserService:
    def __init__(self, crud: CRUDUser):
        self.crud = crud

    async def create(self, user_in: IUserCreate) -> User:
        user = await self.crud.get_by_email(email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {user_in.email} already exists",
            )
        user = await self.crud.create_with_role(obj_in=user_in)
        return user

    async def delete(self, user_id: UUID) -> User | None:
        deleted_user = await self.crud.remove(id=user_id)
        if deleted_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            ) from None
        return deleted_user

    async def update_password_me(self, body: IUserUpdatePassword, current_user: User):
        user = await self.crud.authenticate(
            email=current_user.email, password=body.current_password
        )
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect password")
        if body.current_password == body.new_password:
            raise HTTPException(
                status_code=400,
                detail="New password cannot be the same as the current one",
            )
        hashed_password = get_password_hash(body.new_password)
        new_data = current_user.model_copy()
        new_data.hashed_password = hashed_password
        await self.crud.update(obj_current=current_user, obj_new=new_data)

    async def update_user_me(
        self,
        updated_param: IUserUpdateMe | dict[str, Any],
        current_user: User,
    ) -> User | None:
        if updated_param.dict(exclude_none=True) == {}:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="At least one parameter for user update info should be provided",
            )

        updated_user = await self.crud.update_user_me(
            obj_in=updated_param, user=current_user
        )
        return updated_user

    async def update_user(
        self,
        target_user_id: UUID,
        updated_param: IUserUpdate | dict[str, Any],
    ) -> User | None:
        if updated_param.dict(exclude_none=True) == {}:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="At least one parameter for user update info should be provided",
            )
        if updated_param.email:
            user = await self.crud.get_by_email(email=updated_param.email)
            if user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User with email {updated_param.email} already exists",
                )
        user_to_update = await self.crud.get(id=target_user_id)
        return await self.crud.update_from_admin_role(
            obj_in=updated_param, user=user_to_update
        )

    async def read_user_by_id(self, user_id: UUID) -> User | None:
        user = await self.crud.get(id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
        return user

    async def read_users_by_role_name(self, user_status, role_name, name, params):
        user_status = True if user_status == IUserStatus.active else False
        query = (
            select(User)
            .join(Role, User.role_id == Role.id)
            .where(
                and_(
                    col(Role.name).ilike(f"%{role_name}%"),
                    User.is_active == user_status,
                    or_(
                        col(User.name).ilike(f"%{name}%"),
                        col(User.surname).ilike(f"%{name}%"),
                    ),
                )
            )
            .order_by(User.name)
        )
        return await self.crud.get_multi_paginated(query=query, params=params)
