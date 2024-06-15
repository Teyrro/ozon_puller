from collections.abc import Sequence

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models import User
from app.models.ozon_report_model import OzonReport
from app.schemas.ozon_report_schema import IOzonReportCreate, IOzonReportUpdate
from app.schemas.ozon_requests_schema import ReportType


class CRUDOzonReport(CRUDBase[OzonReport, IOzonReportCreate, IOzonReportUpdate]):
    async def get_last_item_by_created_at(
        self, *, db_session: AsyncSession | None = None
    ) -> OzonReport | None:
        stmt = (
            select(OzonReport)
            .where(OzonReport.report_type == ReportType.seller_products.lower())
            .order_by(desc(OzonReport.ozon_created_at))
            .limit(1)
        )
        session = db_session or self.db.session
        ozon_info = await session.execute(stmt)
        return ozon_info.scalar_one_or_none()

    async def create_seller_report_for_all_users(
        self,
        *,
        users: Sequence[User],
        report: IOzonReportCreate,
        db_session: AsyncSession | None = None,
    ):
        session = db_session or self.db.session
        report = OzonReport.model_validate(report)
        report.user = users
        session.add(report)
        await session.commit()

    async def get_last_by_report_type(
        self, *, type: ReportType, db_session: AsyncSession | None = None
    ):
        stmt = (
            select(OzonReport)
            .where(OzonReport.report_type == type)
            .order_by(desc(OzonReport.created_at))
            .limit(1)
        )
        session = db_session or self.db.session
        metrics = await session.execute(stmt)
        return metrics.scalar_one_or_none()


ozon_report = CRUDOzonReport(OzonReport)
