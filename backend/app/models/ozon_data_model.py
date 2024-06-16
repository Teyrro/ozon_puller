from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from user_models import User


class OzonDataBase(SQLModel):
    client_id: str = Field(nullable=False)
    api_key: str = Field(nullable=False)


class OzonDataWithUserID(OzonDataBase):
    user_id: UUID | None = Field(
        nullable=False, foreign_key="User.id", unique=True, default=None
    )


class OzonData(BaseUUIDModel, OzonDataWithUserID, table=True):
    user: "User" = Relationship(
        back_populates="ozon_confidential",
        sa_relationship_kwargs={"lazy": "selectin", "uselist": False},
    )
