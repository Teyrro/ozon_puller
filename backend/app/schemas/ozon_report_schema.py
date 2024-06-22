from datetime import datetime
from uuid import UUID

from sqlmodel import Field

from app.models.ozon_report_model import OzonReportBase
from app.utils.partial import partial_model


class IOzonReportCreate(OzonReportBase):
    pass


class IOzonReportRead(OzonReportBase):
    id: UUID
    report: bytes = Field(exclude=True)
    created_at: datetime | None


# All these fields are optional
@partial_model
class IOzonReportUpdate(OzonReportBase):
    pass
