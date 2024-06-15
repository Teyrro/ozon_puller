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

ozon_data_router = APIRouter()


@ozon_data_router.delete("/")
async def remove_ozon_data(id) -> IDeleteResponseBase[IOzonDataRead]:
    removed_ozon_data = await crud.ozon_data.remove(id=id)
    return create_response(removed_ozon_data, message="Ozon Credentials removed")


@ozon_data_router.post("/")
async def create_ozon_data(
    ozon_data_in: IOzonDataCreate, current_user: UserAuthDep
) -> IPostResponseBase[IOzonDataRead]:
    try:
        ozon_data_out = await crud.ozon_data.create_credentials(
            id=current_user.id, obj_in=ozon_data_in
        )
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ozon Credentials already exists",
        ) from err
    return create_response(ozon_data_out)


@ozon_data_router.patch("/")
async def update_ozon_data_me(
    update_params: IOzonDataUpdate, current_user: UserAuthDep
) -> IGetResponseBase[IOzonDataRead]:
    current_ozon_data = await crud.ozon_data.get_by_user_id(id=current_user.id)
    updated_ozon_data = await crud.ozon_data.update_credentials(
        update_params=update_params, obj_in=current_ozon_data
    )
    return create_response(data=updated_ozon_data, message="Ozon Credentials updated")


@ozon_data_router.get("/")
async def read_ozon_data_me(
    current_user: UserAuthDep,
) -> IGetResponseBase[IOzonDataRead]:
    try:
        ozon_data = await crud.ozon_data.get_by_user_id(id=current_user.id)
        return create_response(ozon_data)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Ozon Data not found")
