from enum import Enum

from pydantic import BaseModel, ConfigDict
from sqlmodel import SQLModel

from app.schemas.role_schema import IRoleRead


class TunedModel(SQLModel):
    """tells pydantic to convert even non dict obj to json"""

    model_config = ConfigDict(from_attributes=True)


class IMetaGeneral(BaseModel):
    roles: list[IRoleRead]


class IOrderEnum(str, Enum):
    ascendant = "ascendant"
    descendent = "descendent"


class TokenType(str, Enum):
    ACCESS = "access_token"
