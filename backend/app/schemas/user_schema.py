import re
from enum import Enum
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, constr, field_validator
from starlette import status

from app.models.user_models import UserBase
from app.schemas.base_schema import TunedModel
from app.schemas.role_schema import IRoleRead
from app.utils.partial import partial_model

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class NameSurnameValidator(BaseModel):
    name: str
    surname: str

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Name should contains only letters",
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Surname should contains only letters",
            )
        return value


class IUserCreate(NameSurnameValidator, UserBase):
    password: str
    model_config = ConfigDict()


class IUserRead(TunedModel, UserBase):
    id: UUID
    role: IRoleRead | None = None


@partial_model
class IUserUpdate(UserBase):
    pass


class IUserUpdateMe(NameSurnameValidator, BaseModel):
    name: constr(min_length=1) | None = None
    surname: constr(min_length=1) | None = None


class IUserUpdatePassword(BaseModel):
    current_password: str
    new_password: str


class IUserBasicInfo(BaseModel):
    id: UUID
    first_name: str
    last_name: str


class IUserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
