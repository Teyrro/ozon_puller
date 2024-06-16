from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from app import crud
from app.api.deps import UserAuthDep
from app.schemas.ozon_data_schema import IOzonDataCreate, IOzonDataRead, IOzonDataUpdate
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IPostResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleEnum

ozon_data_router = APIRouter()


@ozon_data_router.delete(
    "/{ozon_data_id}",
)
async def remove_ozon_data(
    ozon_data_id: UUID, current_user: UserAuthDep
) -> IDeleteResponseBase[IOzonDataRead]:
    current_ozon_data = await crud.ozon_data.get(id=ozon_data_id)
    if current_ozon_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ozon Credentials does not exist",
        )
    if current_user.role.name == IRoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin can't remove ozon credentials.",
        )
    removed_ozon_data = await crud.ozon_data.remove(id=ozon_data_id)
    return create_response(removed_ozon_data, message="Ozon Credentials removed")


@ozon_data_router.post("/")
async def create_ozon_data(
    ozon_data_in: IOzonDataCreate, current_user: UserAuthDep
) -> IPostResponseBase[IOzonDataRead]:
    try:
        current_ozon_data = await crud.ozon_data.get_by_user_id(id=current_user.id)
        if current_ozon_data:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ozon Credentials already exists",
            )
        ozon_data_out = await crud.ozon_data.create_credentials(
            id=current_user.id, obj_in=ozon_data_in
        )
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database error {err}",
        ) from err
    return create_response(ozon_data_out)


@ozon_data_router.patch("/me")
async def update_ozon_data_me(
    update_params: IOzonDataUpdate, current_user: UserAuthDep
) -> IGetResponseBase[IOzonDataRead]:
    current_ozon_data = current_user.ozon_confidential
    if current_ozon_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ozon Credentials does not exist",
        )
    updated_ozon_data = await crud.ozon_data.update_credentials(
        obj_in=current_ozon_data, update_params=update_params
    )
    return create_response(data=updated_ozon_data, message="Ozon Credentials updated")


@ozon_data_router.get("/me")
async def read_ozon_data_me(
    current_user: UserAuthDep,
) -> IGetResponseBase[IOzonDataRead]:
    try:
        ozon_data = await crud.ozon_data.get_by_user_id(id=current_user.id)
        if ozon_data is None:
            raise HTTPException(status_code=404, detail="Ozon Data not found")
        return create_response(ozon_data)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {err}",
        ) from err
