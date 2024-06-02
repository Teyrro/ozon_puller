from typing import TYPE_CHECKING

from sqlmodel import Relationship, SQLModel

from app.models.base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from user_models import User


class RoleBase(SQLModel):
    name: str
    description: str


class Role(BaseUUIDModel, RoleBase, table=True):
    users: list["User"] = Relationship(  # noqa: F821
        back_populates="role", sa_relationship_kwargs={"lazy": "selectin"}
    )
