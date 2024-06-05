from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core import security
from app.core.config import settings
from app.schemas.ozon_data_schema import IOzonDataCreate
from app.schemas.role_schema import IRoleCreate
from app.schemas.user_schema import IUserCreate

roles: list[IRoleCreate] = [
    IRoleCreate(name="admin", description="This the Admin role"),
    IRoleCreate(name="manager", description="Manager role"),
    IRoleCreate(name="user", description="User role"),
]

users: list[dict[str, str | IUserCreate]] = [
    {
        "data": IUserCreate(
            name="Admin",
            surname="FastAPI",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            email=settings.FIRST_SUPERUSER_EMAIL,
        ),
        "role": "admin",
    },
    # {
    #     "data": IUserCreate(
    #         name="Manager",
    #         surname="FastAPI",
    #         password=settings.FIRST_SUPERUSER_PASSWORD,
    #         email="manager@example.com",
    #
    #     ),
    #     "role": "manager",
    # },
    # {
    #     "data": IUserCreate(
    #         name="User",
    #         surname="FastAPI",
    #         password=settings.FIRST_SUPERUSER_PASSWORD,
    #         email="user@example.com",
    #     ),
    #     "role": "user",
    # },
]

ozon_data: list[dict[str, IOzonDataCreate]] = [
    {
        "data": IOzonDataCreate(
            client_id=settings.FIRST_SUPERUSER_CLIENT_ID,
            api_key=settings.FIRST_SUPERUSER_API_KEY,
        )
    }
]


async def init_db(session: AsyncSession) -> None:
    for role in roles:
        role_current = await crud.role.get_role_by_name(
            name=role.name, db_session=session
        )
        if not role_current:
            await crud.role.create(obj_in=role, db_session=session)

    for user in users:
        current_user = await crud.user.get_by_email(
            email=user["data"].email, db_session=session
        )
        role = await crud.role.get_role_by_name(name=user["role"], db_session=session)

        if not current_user:
            user["data"].role_id = role.id
            await crud.user.create_with_role(obj_in=user["data"], db_session=session)

    for conf_data in ozon_data:
        count_tuples = bool(await crud.ozon_data.get_count(session))

        admin_user = await crud.user.get_by_email(
            email=settings.FIRST_SUPERUSER_EMAIL, db_session=session
        )
        if not count_tuples:
            conf_data["data"].user_id = admin_user.id
            conf_data["data"].api_key = security.get_data_encrypt(conf_data["data"].api_key)
            await crud.ozon_data.create(obj_in=conf_data["data"], db_session=session)
