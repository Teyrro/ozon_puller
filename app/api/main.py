from fastapi import APIRouter

from app.api.routes.login import login_router
from app.api.routes.users import user_router

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
