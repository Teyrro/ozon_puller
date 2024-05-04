from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.routes.action.login import get_user_by_email_for_auth
from app.core.config import settings
from app.db.models import User
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

TokenDep = Annotated[str, Depends(oauth2_scheme)]

SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user_from_token(token: TokenDep, session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        print("username/email extracted is ", email)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email_for_auth(email, session)
    if user is None:
        raise credentials_exception
    return user


UserAuthDep = Annotated[User, Depends(get_current_user_from_token)]


def get_current_active_superadmin(current_user: UserAuthDep) -> User:
    if not current_user.is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user don't have enough privileges",
        )
    return current_user
