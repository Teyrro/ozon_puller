from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.deps import SessionDep, get_db
from app.api.models import (
    DeleteUserResponse,
    ShowUser,
    UpdatedUserResponse,
    UpdateUserRequest,
    UserCreate,
)
from app.api.routes.action.users import (
    _create_new_user,
    _delete_new_user,
    _get_user_by_id,
    _update_user,
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
    user_id: UUID, session: AsyncSession = Depends(get_db)
) -> DeleteUserResponse:
    deleted_user_id = await _delete_new_user(user_id, session)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        ) from None
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, session: SessionDep) -> ShowUser:
    user = await _get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID, body: UpdateUserRequest, session: SessionDep
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user = await _get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=session, user_id=user_id
        )
    except IntegrityError as err:
        # logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err

    return UpdatedUserResponse(updated_user_id=updated_user_id)
