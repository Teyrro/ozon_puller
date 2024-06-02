from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.routes.servises.login import LoginService
from app.schemas.token_schema import Token

login_router = APIRouter()


@login_router.post("/access-token", response_model=Token)
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    login_service = LoginService(crud.user)
    return await login_service.authenticate_user(form_data)
