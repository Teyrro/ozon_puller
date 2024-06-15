from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

from app import crud
from app.api import deps
from app.deps import role_deps
from app.models.role_model import Role
from app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleCreate, IRoleEnum, IRoleRead, IRoleUpdate
from app.utils.exceptions.common_exceptions import (
    ContentNoChangeException,
    NameExistException,
)

role_router = APIRouter()


@role_router.get(
    "",
    response_model=IGetResponsePaginated[IRoleRead],
    dependencies=[Depends(deps.get_current_user())],
)
async def get_roles(
    params: Params = Depends(),
) -> Any:
    """
    Gets a paginated list of roles
    """
    roles = await crud.role.get_multi_paginated(params=params)
    return create_response(data=roles, message="Roles fetched successfully")


@role_router.get(
    "/{role_id}",
    dependencies=[Depends(deps.get_current_user())],
    response_model=IGetResponseBase[IRoleRead],
)
async def get_role_by_id(
    role: Role = Depends(role_deps.get_user_role_by_id),
) -> Any:
    """
    Gets a role by its id
    """
    return create_response(data=role, message="Role retrieved successfully")


@role_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=IPostResponseBase[IRoleRead],
    dependencies=[Depends(deps.get_current_user([IRoleEnum.admin]))],
)
async def create_role(
    role: IRoleCreate,
) -> Any:
    """
    Create a new role

    Required roles:
    - admin
    """
    role_current = await crud.role.get_role_by_name(name=role.name)
    if role_current:
        raise NameExistException(Role, name=role_current.name)

    new_role = await crud.role.create(obj_in=role)
    return create_response(data=new_role, message="Role created successfully")


@role_router.put(
    "/{role_id}",
    response_model=IPutResponseBase[IRoleRead],
    dependencies=[Depends(deps.get_current_user([IRoleEnum.admin]))],
)
async def update_role(
    role: IRoleUpdate,
    current_role: Role = Depends(role_deps.get_user_role_by_id),
) -> Any:
    """
    Updates a role by its id

    Required roles:
    - admin
    """
    if current_role.description == role.description:
        raise ContentNoChangeException()

    updated_role = await crud.role.update(obj_current=current_role, obj_new=role)
    return create_response(data=updated_role, message="Role updated!")
