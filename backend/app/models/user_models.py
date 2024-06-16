from typing import TYPE_CHECKING, Optional
from uuid import UUID

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
    role_id: UUID | None = Field(nullable=False, foreign_key="Role.id", default=None)


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str | None = Field(nullable=False, index=True, default=None)
    role: Optional["Role"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False},
    )

    ozon_confidential: Optional["OzonData"] = Relationship(
        sa_relationship_kwargs={
            "back_populates": "user",
            "cascade": "all, delete, delete-orphan",
            "lazy": "joined",
        }
    )
    ozon_reports: list["OzonReport"] = Relationship(
        back_populates="user",
        link_model=LinkUserOzonReport,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
