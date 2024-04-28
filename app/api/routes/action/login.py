from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hashing import Hasher
from app.db.dals import get_user_by_email
from app.db.models import User


async def get_user_by_email_for_auth(email: str, session: AsyncSession):
    async with session.begin():
        return await get_user_by_email(email=email, session=session)


async def authenticate_user(
    email: str, password: str, session: AsyncSession
) -> User | None:
    user = await get_user_by_email_for_auth(email, session)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user
