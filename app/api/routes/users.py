from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Params, add_pagination
from sqlalchemy.exc import IntegrityError
from starlette import status

from app import crud
from app.api import deps
from app.api.deps import UserAuthDep
from app.api.routes.servises.users import UserService
from app.deps import user_deps
from app.models import Role, User
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    MessageResponse,
    create_response,
)
from app.schemas.role_schema import IRoleEnum
from app.schemas.user_schema import (
    IUserCreate,
    IUserRead,
    IUserStatus,
    IUserUpdateMe,
    IUserUpdatePassword,
)
from app.utils.exceptions.common_exceptions import IdNotFoundException
from app.utils.exceptions.user_exceptions import UserSelfDeleteException

# logger = getLogger(__name__)

user_router = APIRouter()
add_pagination(user_router)


@user_router.post("/",
                  status_code=status.HTTP_201_CREATED,
                  dependencies=[Depends(deps.get_current_user([IRoleEnum.admin]))])
async def create_user(
        user_in: IUserCreate,
) -> IPostResponseBase[IUserRead]:
    """
    Create User

    Required roles:
    - admin
    """
    try:
        role = await crud.role.get(id=user_in.role_id)
        if not role:
            raise IdNotFoundException(Role, id=user_in.role_id)
        user_service = UserService(crud.user)
        user = await user_service.create(user_in)
        return create_response(data=user)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error {err}",
        ) from err


@user_router.get(
    "/me"
)
async def read_user_me(current_user: UserAuthDep) -> IGetResponseBase[IUserRead]:
    """
    Get current user.
    """
    return create_response(data=current_user)


@user_router.get(
    "/{user_id}",
    dependencies=[Depends(deps.get_current_user([IRoleEnum.admin]))],
)
async def read_user_by_id(
        user_id: UUID
) -> IGetResponseBase[IUserRead]:
    """
    Get user by id

    Required roles:
    - admin
    """
    user_service = UserService(crud.user)
    user = await user_service.read_user_by_id(user_id)
    return create_response(data=user)


@user_router.get(
    "/list/",
    dependencies=[Depends(deps.get_current_user([IRoleEnum.admin]))]
)
async def read_users(params: Params = Depends()) -> IGetResponsePaginated[IUserRead]:
    """
    Retrieve users.

    Required roles:
    - admin
    """
    users = await crud.user.get_multi_paginated(params=params)
    return create_response(data=users)


@user_router.get(
    "/list/by_role_name",
    dependencies=[Depends(
        deps.get_current_user([IRoleEnum.admin]))],
    response_model=IGetResponsePaginated[IUserRead]
)
async def read_users_list_by_role_name(
        name: str = "",
        user_status: Annotated[
            IUserStatus,
            Query(
                title="User status",
                description="User status, It is optional. Default is active",
            ),
        ] = IUserStatus.active,
        role_name: str = "",
        params: Params = Depends(),
) -> Any:
    """
    Retrieve users by role name and status. Requires admin role

    Required roles:
    - admin
    """
    user_service = UserService(crud.user)
    try:
        users = await user_service.read_users_by_role_name(user_status,
                                                           role_name,
                                                           name,
                                                           params)
        return create_response(data=users)
    except IntegrityError as err:
        print(err)



@user_router.get(
    "/order_by_created_at/",
    dependencies=[
        Depends(
            deps.get_current_user(
                [IRoleEnum.admin,
                 IRoleEnum.manager]))
    ]
)
async def get_user_list_order_by_created_at(
        params: Params = Depends(),
) -> IGetResponsePaginated[IUserRead]:
    """
    Gets a paginated list of users ordered by created datetime

    Required roles:
    - admin
    - manager
    """
    users = await crud.user.get_multi_paginated_ordered(
        params=params, order_by="created_at"
    )
    return create_response(data=users)


@user_router.delete("/{user_id}")
async def delete_user(
        user_id: UUID = Depends(user_deps.is_valid_user_id),
        current_user: User = Depends(
            deps.get_current_user(required_roles=[IRoleEnum.admin])
        ),
) -> IDeleteResponseBase[IUserRead]:
    """
    Delete user

    Required roles:
    - admin
    """
    user_service = UserService(crud.user)
    if current_user.id == user_id:
        raise UserSelfDeleteException()

    deleted_user = await user_service.delete(user_id)
    return create_response(data=deleted_user)


@user_router.patch(
    "/me/password")
async def update_password_me(
        *, body: IUserUpdatePassword, current_user: UserAuthDep
) -> MessageResponse:
    """
    Update own password.
    """
    user_service = UserService(crud.user)
    await user_service.update_password_me(body, current_user)
    return MessageResponse(message="Password updated successfully")


@user_router.patch(
    "/me"
)
async def update_user_me(
        body: IUserUpdateMe,
        current_user: UserAuthDep,
) -> IPutResponseBase[IUserRead]:
    user_service = UserService(crud.user)
    try:
        updated_user = await user_service.update_user_me(
            updated_param=body, current_user=current_user
        )
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {err}",
        ) from err

    return create_response(data=updated_user)
