from datetime import timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.core.config import settings
from app.core.security import create_access_token
from app.crud.user_crud import CRUDUser
from app.schemas.token_schema import Token


class LoginService:

    def __init__(self, u_crud: CRUDUser):
        self.user_crud = u_crud

    async def authenticate_user(
        self, form_data: OAuth2PasswordRequestForm
    ) -> Token | None:
        user = await self.user_crud.authenticate(email=form_data.username, password=form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email or Password incorrect")
        elif not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(user.id, expires_delta=access_token_expires)
        )
