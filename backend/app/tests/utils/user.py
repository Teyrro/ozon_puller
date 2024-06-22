from collections.abc import Coroutine
from datetime import datetime
from typing import Any
from uuid import UUID

from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.db.session import SessionLocal
from app.schemas.ozon_data_schema import IOzonDataCreate
from app.schemas.ozon_report_schema import IOzonReportCreate
from app.schemas.ozon_requests_schema import ReportType
from app.schemas.role_schema import IRoleEnum
from app.schemas.user_schema import IUserCreate
from app.tests.utils.utils import random_email, random_lower_string
from app.utils.getURL import getURL


async def user_authentication_headers(
    *, client: AsyncClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}
    url = await getURL("/login/access-token")
    r = await client.post(url, data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def get_role_id(role: IRoleEnum, db: AsyncSession | None = None) -> UUID:
    role = await crud.role.get_role_by_name(name=role, db_session=db)
    return role.id


async def create_random_user(
    db: AsyncSession,
    name: str | None = None,
    surname: str | None = None,
    role: IRoleEnum = IRoleEnum.user,
):
    email = random_email()
    password = random_lower_string()
    role_id = await get_role_id(role=role, db=db)
    if name is None:
        name = "Michel"
    if surname is None:
        surname = "Far"
    user_in = IUserCreate(
        name=name,
        surname=surname,
        email=email,
        password=password,
        is_active=True,
        role_id=role_id,
    )
    user = await crud.user.create_with_role(db_session=db, obj_in=user_in)
    return user, password


async def create_random_ozon_data(
    db: AsyncSession,
):
    user_in, pswd = await create_random_user(db=db)
    client_id = random_lower_string()
    api_key = random_lower_string()
    ozon_in = IOzonDataCreate(
        api_key=api_key,
        client_id=client_id,
    )
    ozon_out = await crud.ozon_data.create_credentials(
        db_session=db, id=user_in.id, obj_in=ozon_in
    )
    return ozon_out, user_in, pswd


async def create_random_file(
    db: AsyncSession,
):
    file = b"Hello World"
    users = await crud.user.get_all_id(db_session=db)
    orm_report = IOzonReportCreate(
        report=file,
        ozon_created_at=datetime.now(),
        report_type=ReportType.seller_products.lower(),
    )
    report = await crud.ozon_report.create_seller_report_for_all_users(
        users=users,
        report=orm_report,
        db_session=db,
    )
    return report


async def authentication_token_from_email(
    *, client: AsyncClient, email: str, db: SessionLocal, role: IRoleEnum
) -> Coroutine[Any, Any, dict[str, str]]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = await crud.user.get_by_email(db_session=db, email=email)
    if not user:
        user = await create_random_user(db=db, role=role)

    return user_authentication_headers(client=client, email=email, password=password)
