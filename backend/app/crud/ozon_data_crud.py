from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models import OzonData
from app.schemas.ozon_data_schema import IOzonDataCreate, IOzonDataUpdate


class CRUDOzonData(CRUDBase[OzonData, IOzonDataCreate, IOzonDataUpdate]):
    async def get_by_user_id(self, *, id, db_session: AsyncSession | None = None):
        stmt = select(OzonData).where(OzonData.user_id == id)
        session = db_session or self.db.session
        ozon_info = await session.execute(stmt)
        return ozon_info.scalar_one_or_none()


ozon_data = CRUDOzonData(OzonData)
