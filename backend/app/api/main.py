from fastapi import APIRouter

from app.api.routes.login import login_router
from app.api.routes.ozon_request import ozon_request_router
from app.api.routes.report import report_router
from app.api.routes.role import role_router
from app.api.routes.users import user_router
from app.core.config import ModeEnum, settings

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(report_router, prefix="/report", tags=["report"])
main_api_router.include_router(role_router, prefix="/role", tags=["role"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
if settings.ENVIRONMENT == ModeEnum.development:
    main_api_router.include_router(ozon_request_router, prefix="/ozon", tags=["ozon"])
