from typing import Any, Generic, TypeVar
from uuid import UUID

from fastapi_pagination.links import Page
from pydantic import BaseModel

from app.models.user_models import UserBase


class MessageResponse(BaseModel):
    message: str


class IUserDeleteResponse(UserBase):
    id: UUID


class IUserUpdatedResponse(UserBase):
    id: UUID


DataType = TypeVar("DataType")
T = TypeVar("T")


class PageBase(Page[T], Generic[T]):
    pass


class IResponseBase(BaseModel, Generic[T]):
    message: str = ""
    meta: dict | Any | None = {}
    data: T | None = None


class IGetResponsePaginated(Page[T], Generic[T]):
    message: str | None = "Data got correctly"
    meta: dict | Any | None = {}


class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data got correctly"


class IPostResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data created correctly"


class IPutResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data updated correctly"


class IDeleteResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data deleted correctly"


def create_response(
    data: DataType,
    message: str | None = None,
    meta: dict | Any | None = None,
) -> (
    IResponseBase[DataType]
    | IGetResponsePaginated[DataType]
    | IGetResponseBase[DataType]
    | IPutResponseBase[DataType]
    | IDeleteResponseBase[DataType]
    | IPostResponseBase[DataType]
):
    if meta is None:
        meta = {}
    if isinstance(data, IGetResponsePaginated):
        data.message = "Data paginated correctly" if message is None else message
        data.meta = meta
        return data
    if message is None:
        return {"data": data, "meta": meta}
    return {"data": data, "message": message, "meta": meta}
