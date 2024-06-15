from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import security
from app.crud.base_crud import CRUDBase
from app.models import OzonData
from app.schemas.ozon_data_schema import IOzonDataCreate, IOzonDataUpdate


class CRUDOzonData(CRUDBase[OzonData, IOzonDataCreate, IOzonDataUpdate]):
    async def update_credentials(
        self,
        *,
        update_params: IOzonDataUpdate,
        obj_in: OzonData,
        db_session: AsyncSession | None = None,
    ) -> OzonData:
        update_params = update_params.model_dump(exclude_unset=True)
        obj_out = obj_in.sqlmodel_update(update_params).copy()
        if update_params["api_key"]:
            update_params["api_key"] = await security.get_data_encrypt(
                update_params["api_key"]
            )
        obj_in.sqlmodel_update(update_params)

        db_session = db_session or self.db.session
        db_session.add(obj_in)
        await db_session.commit()
        await db_session.refresh(obj_in)

        return obj_out

    async def get_by_user_id(
        self, *, id, db_session: AsyncSession | None = None
    ) -> OzonData | None:
        session = db_session or self.db.session
        stmt = select(OzonData).where(OzonData.user_id == id)
        ozon_info = await session.execute(stmt)
        data: OzonData = ozon_info.scalar_one_or_none()
        if data is None:
            return
        data_out: OzonData = data.copy()
        data_out.api_key = await security.get_context(data_out.api_key)
        return data_out

    async def create_credentials(
        self,
        *,
        id: UUID,
        obj_in: IOzonDataCreate,
        db_session: AsyncSession | None = None,
    ) -> OzonData:
        db_session = db_session or self.db.session
        db_obj = OzonData.model_validate(obj_in, update={"user_id": id})

        obj_out = db_obj.copy()
        db_obj.api_key = await security.get_data_encrypt(obj_in.api_key)
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return obj_out


ozon_data = CRUDOzonData(OzonData)
