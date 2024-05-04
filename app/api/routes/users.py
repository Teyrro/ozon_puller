from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.api.deps import SessionDep, UserAuthDep, get_current_active_superadmin
from app.api.models import (
    DeleteUserResponse,
    ShowUser,
    UpdatedUserResponse,
    UpdateUserRequest,
    UserCreate,
)
from app.api.routes.action.users import (
    RequestAction,
    _create_new_user,
    _delete_new_user,
    _get_user_by_id,
    _update_user,
    check_user_permissions,
)

# logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: SessionDep) -> ShowUser:
    try:
        return await _create_new_user(user, db)
    except IntegrityError as err:
        # logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error {err}",
        ) from err


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID, session: SessionDep, current_user: UserAuthDep
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, session)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    if not check_user_permissions(
        target_user=user_for_deletion,
        current_user=current_user,
        action=RequestAction.DELETE,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )
    deleted_user_id = await _delete_new_user(user_id, session)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        ) from None
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.patch(
    "/admin_privilege",
    response_model=UpdatedUserResponse,
    dependencies=[Depends(get_current_active_superadmin)],
)
async def grant_admin_privilege(
    user_id: UUID,
    db: SessionDep,
    current_user: UserAuthDep,
):
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Cannot manage privileges of itself."
        )
    user_for_promotion = await _get_user_by_id(user_id, db)
    if user_for_promotion.is_admin or user_for_promotion.is_superadmin:
        raise HTTPException(
            status_code=409,
            detail=f"User with id {user_id} already promoted to admin / superadmin.",
        )
    if user_for_promotion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    updated_user_params = {"roles": user_for_promotion.promote_to_admin()}
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.delete(
    "/admin_privilege",
    response_model=UpdatedUserResponse,
    dependencies=[Depends(get_current_active_superadmin)],
)
async def revoke_admin_privilege(
    user_id: UUID,
    db: SessionDep,
    current_user: UserAuthDep,
):
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Cannot manage privileges of itself."
        )
    user_for_revoke_admin_privileges = await _get_user_by_id(user_id, db)
    if not user_for_revoke_admin_privileges.is_admin:
        raise HTTPException(
            status_code=409, detail=f"User with id {user_id} has no admin privileges."
        )
    if user_for_revoke_admin_privileges is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    updated_user_params = {
        "roles": user_for_revoke_admin_privileges.remove_admin_privilege()
    }
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID, session: SessionDep, current_user: UserAuthDep
) -> ShowUser:
    user = await _get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return ShowUser(
        user_id=user.user_id,
        name=user.name,
        surname=user.surname,
        email=user.email,
        is_active=user.is_active,
    )


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequest,
    session: SessionDep,
    current_user: UserAuthDep,
) -> Any:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await _get_user_by_id(user_id, session)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if not check_user_permissions(
        target_user=user_for_update,
        current_user=current_user,
        action=RequestAction.UPDATE,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )

    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=session, user_id=user_id
        )
    except IntegrityError as err:
        # logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err

    return UpdatedUserResponse(updated_user_id=updated_user_id)
