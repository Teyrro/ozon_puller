from uuid import UUID

from sqlmodel import Field

from app.models.base_uuid_model import BaseUUIDModel


class LinkUserOzonReport(BaseUUIDModel, table=True):
    user_id: UUID | None = Field(
        default=None, nullable=False, foreign_key='User.id', primary_key=True
    )
    ozon_report_id: UUID | None = Field(
        default=None, nullable=False, foreign_key='OzonReport.id', primary_key=True
    )
