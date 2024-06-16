from collections.abc import Sequence
from uuid import UUID

from pydantic.networks import EmailStr
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base_crud import CRUDBase
from app.models import Role, User
from app.schemas.role_schema import IRoleEnum
from app.schemas.user_schema import IUserCreate, IUserUpdate, IUserUpdateMe


class CRUDUser(CRUDBase[User, IUserCreate, IUserUpdate]):
    async def get_by_email(
        self, *, email: str, db_session: AsyncSession | None = None
    ) -> User | None:
        db_session = db_session or self.db.session
        users = await db_session.execute(select(User).where(User.email == email))
        return users.scalar_one_or_none()

    async def get_by_id_active(self, *, id: UUID) -> User | None:
        user = await self.get(id=id)
        if not user:
            return None
        if user.is_active is False:
            return None
        return user

    async def update_user_me(
        self, obj_in: IUserUpdateMe, user: User, db_session: AsyncSession | None = None
    ) -> User:
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        user.sqlmodel_update(obj_in_data)

        db_session = db_session or self.db.session
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    # async def update_with_oz_data(
    #         self, *, obj_in: IUserUpdateMe, user: User, db_session: AsyncSession | None = None
    # ) -> User:
    #     obj_in_data = obj_in.model_dump(exclude_unset=True)
    #     user.sqlmodel_update(obj_in_data)
    #     return await self._update_value(obj_in, user, db_session)

    async def update_from_admin_role(
        self, *, obj_in: IUserUpdate, user: User, db_session: AsyncSession | None = None
    ) -> User:
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        if obj_in.password is not None:
            hashed_pswd = {"hashed_password": get_password_hash(obj_in.password)}
            user.sqlmodel_update(obj_in_data, update=hashed_pswd)
        else:
            user.sqlmodel_update(obj_in_data)
        db_session = db_session or self.db.session
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    async def create_with_role(
        self, *, obj_in: IUserCreate, db_session: AsyncSession | None = None
    ) -> User:
        db_session = db_session or self.db.session
        db_obj = User.model_validate(obj_in)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def authenticate(self, *, email: EmailStr, password: str) -> User | None:
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def remove(
        self, *, id: UUID | str, db_session: AsyncSession | None = None
    ) -> User:
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = response.scalar_one_or_none()
        await db_session.delete(obj)
        await db_session.commit()
        return obj

    async def get_admin_id(self, db_session: AsyncSession | None = None) -> UUID:
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(User, Role)
            .where(and_(User.role_id == Role.id, Role.name == IRoleEnum.admin))
            .limit(1)
        )
        obj = response.scalar_one_or_none()
        if obj is not None:
            return obj.id

    async def get_all_id(
        self, db_session: AsyncSession | None = None
    ) -> Sequence[User]:
        db_session = db_session or self.db.session
        response = await db_session.execute(select(User))
        obj = response.scalars().all()
        if obj is not None:
            return obj


user = CRUDUser(User)
