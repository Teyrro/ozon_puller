import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlmodel import AutoString, Field, Relationship, SQLModel

from app.models.base_uuid_model import BaseUUIDModel
from app.models.links_model import LinkUserOzonReport

if TYPE_CHECKING:
    from ozon_data_model import OzonData
    from ozon_report_model import OzonReport
    from role_model import Role


class UserBase(SQLModel):
    name: str
    surname: str
    email: EmailStr = Field(nullable=False, unique=True, index=True, sa_type=AutoString)
    is_active: bool = Field(default=True)
    role_id: uuid.UUID | None = Field(default=None, foreign_key="Role.id")


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str | None = Field(nullable=False, index=True, default=None)
    role: Optional["Role"] = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "joined"}
    )

    ozon_confidential: "OzonData" = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    ozon_reports: list["OzonReport"] = Relationship(
        back_populates="user",
        link_model=LinkUserOzonReport,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

