from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, LargeBinary
from sqlmodel import Field, Relationship, SQLModel

from app.models.base_uuid_model import BaseUUIDModel
from app.models.links_model import LinkUserOzonReport

if TYPE_CHECKING:
    from user_models import User


class OzonReportBase(SQLModel):
    report_type: str = Field(nullable=False)
    report: bytes = Field(sa_column=Column(LargeBinary(), nullable=False))
    ozon_created_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True)))


class OzonReport(BaseUUIDModel, OzonReportBase, table=True):
    user: list["User"] = Relationship(
        back_populates="ozon_reports",
        link_model=LinkUserOzonReport,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
