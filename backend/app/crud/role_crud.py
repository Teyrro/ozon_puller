from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models import Role, User
from app.schemas.role_schema import IRoleCreate, IRoleUpdate


class CRUDRole(CRUDBase[Role, IRoleCreate, IRoleUpdate]):
    async def get_role_by_name(
        self, *, name: str, db_session: AsyncSession | None = None
    ) -> Role:
        db_session = db_session or self.db.session
        role = await db_session.execute(select(Role).where(Role.name == name))
        return role.scalar_one_or_none()

    async def add_role_to_user(
        self, *, user: User, role_id: UUID, db_session: AsyncSession | None = None
    ) -> Role:
        db_session = db_session or self.db.session
        role = await self.get(id=role_id, db_session=db_session)
        user.role = role
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return role


role = CRUDRole(Role)
