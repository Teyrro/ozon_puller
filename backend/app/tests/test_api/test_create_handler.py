import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid_extensions import uuid7

from app.schemas.role_schema import IRoleEnum
from app.schemas.user_schema import (
    IUserCreate,
    IUserStatus,
    IUserUpdate,
    IUserUpdateMe,
    IUserUpdatePassword,
)
from app.tests.utils.user import (
    create_random_user,
    get_role_id,
    user_authentication_headers,
)
from app.tests.utils.utils import random_email, random_lower_string
from app.utils.getURL import getURL


async def test_create_user(
    client, async_session_test: AsyncSession, superuser_token_headers
):
    user_in = IUserCreate(
        name="Alex",
        surname="Marser",
        email=random_email(),
        is_active=True,
        password=random_lower_string(),
        role_id=await get_role_id(role=IRoleEnum.user, db=async_session_test),
    )
    url = await getURL("/user/")
    resp = await client.post(
        url, content=user_in.model_dump_json(), headers=superuser_token_headers
    )
    data_from_resp = resp.json()
    data_from_resp = data_from_resp["data"]
    assert resp.status_code == 201
    assert data_from_resp["name"] == user_in.name
    assert data_from_resp["surname"] == user_in.surname
    assert data_from_resp["email"] == user_in.email
    assert data_from_resp["is_active"] is True


async def test_create_user_with_role_admin(
    client, async_session_test: AsyncSession, superuser_token_headers
):
    user_in = IUserCreate(
        name="Alex",
        surname="Marser",
        email=random_email(),
        is_active=True,
        password=random_lower_string(),
        role_id=await get_role_id(role=IRoleEnum.admin, db=async_session_test),
    )
    url = await getURL("/user/")
    resp = await client.post(
        url, content=user_in.model_dump_json(), headers=superuser_token_headers
    )

    assert resp.status_code == 403


async def test_create_user_duplicate_email_error(
    client, async_session_test: AsyncSession, superuser_token_headers
):
    user, pswd = await create_random_user(db=async_session_test)
    user_in = IUserCreate(
        name="Michel",
        surname="Far",
        email=user.email,
        password=random_lower_string(),
        role_id=await get_role_id(role=IRoleEnum.user, db=async_session_test),
    )
    url = await getURL("/user/")
    resp = await client.post(
        url, content=user_in.model_dump_json(), headers=superuser_token_headers
    )
    assert resp.status_code == 409


async def test_create_user_with_invalid_role_id(
    client, async_session_test: AsyncSession, superuser_token_headers
):
    user, pswd = await create_random_user(db=async_session_test)
    role = uuid7()
    user_in = IUserCreate(
        name="Michel",
        surname="Far",
        email=user.email,
        password=random_lower_string(),
        role_id=role,
    )
    url = await getURL("/user/")
    resp = await client.post(
        url, content=user_in.model_dump_json(), headers=superuser_token_headers
    )
    assert resp.status_code == 404


@pytest.mark.parametrize(
    "user_data_for_creation, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": [
                    {
                        "input": {},
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "type": "missing",
                    },
                    {
                        "input": {},
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "type": "missing",
                    },
                    {
                        "input": {},
                        "loc": ["body", "email"],
                        "msg": "Field required",
                        "type": "missing",
                    },
                    {
                        "input": {},
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "type": "missing",
                    },
                ]
            },
        ),
        (
            {"name": 123, "surname": "Sviridov", "email": "lol@kek.com"},
            422,
            {
                "detail": [
                    {
                        "input": 123,
                        "loc": ["body", "name"],
                        "msg": "Input should be a valid string",
                        "type": "string_type",
                    },
                    {
                        "input": {
                            "email": "lol@kek.com",
                            "name": 123,
                            "surname": "Sviridov",
                        },
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "type": "missing",
                    },
                ]
            },
        ),
        (
            {"name": "Nikolai", "surname": 456, "email": "lol@kek.com"},
            422,
            {
                "detail": [
                    {
                        "input": 456,
                        "loc": ["body", "surname"],
                        "msg": "Input should be a valid string",
                        "type": "string_type",
                    },
                    {
                        "input": {
                            "email": "lol@kek.com",
                            "name": "Nikolai",
                            "surname": 456,
                        },
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "type": "missing",
                    },
                ]
            },
        ),
        (
            {"name": "Nikolai", "surname": "Sviridov", "email": "lol"},
            422,
            {
                "detail": [
                    {
                        "ctx": {
                            "reason": "The email address is not valid. It must have "
                            "exactly one @-sign."
                        },
                        "input": "lol",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: The email address is "
                        "not valid. It must have exactly one @-sign.",
                        "type": "value_error",
                    },
                    {
                        "input": {
                            "email": "lol",
                            "name": "Nikolai",
                            "surname": "Sviridov",
                        },
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "type": "missing",
                    },
                ]
            },
        ),
        (
            {"name": "Nikolai12", "surname": "Sviridov", "email": "lol@kek.com"},
            422,
            {"detail": "Name should contains only letters"},
        ),
        (
            {"name": "Nikolai", "surname": "Sviridov12", "email": "lol@kek.com"},
            422,
            {"detail": "Surname should contains only letters"},
        ),
    ],
)
async def test_create_user_validation_error(
    client,
    user_data_for_creation,
    expected_status_code,
    expected_detail,
    superuser_token_headers,
):
    url = await getURL("/user/")
    resp = await client.post(
        url, json=user_data_for_creation, headers=superuser_token_headers
    )
    data_from_resp = resp.json()
    assert resp.status_code == expected_status_code
    assert data_from_resp == expected_detail


async def test_read_user_me(client, async_session_test, superuser_token_headers):
    user, pswd = await create_random_user(db=async_session_test)
    url = await getURL("/user/me")
    token = await user_authentication_headers(
        client=client, email=user.email, password=pswd
    )
    resp = await client.get(url, headers=token)
    assert resp.status_code == 200


async def test_user_by_id(client, async_session_test, superuser_token_headers):
    user, pswd = await create_random_user(db=async_session_test)
    url = await getURL(f"/user/{user.id}")
    resp = await client.get(url, headers=superuser_token_headers)
    assert resp.status_code == 200


async def test_read_users(client, async_session_test, superuser_token_headers):
    url = await getURL("/user/list/")
    resp = await client.get(url, headers=superuser_token_headers)
    assert resp.status_code == 200


async def test_read_users_list_by_role_name(
    client, async_session_test, superuser_token_headers
):
    url = await getURL("/user/list/")
    role_name = IRoleEnum.admin
    body = {"role_name": role_name}
    resp = await client.get(url, params=body, headers=superuser_token_headers)
    assert resp.status_code == 200

    _, _ = await create_random_user(db=async_session_test)
    body = {"role_name": IRoleEnum.user, "user_status": IUserStatus.active}
    resp = await client.get(url, params=body, headers=superuser_token_headers)
    assert resp.status_code == 200


async def test_user_list_order_by_created_at(
    client, async_session_test, superuser_token_headers
):
    url = await getURL("/user/order_by_created_at/")
    resp = await client.get(url, headers=superuser_token_headers)
    assert resp.status_code == 200


async def test_delete_user(client, async_session_test, superuser_token_headers):
    user, pswd = await create_random_user(db=async_session_test)
    url = await getURL(f"/user/delete/{user.id}")
    resp = await client.delete(url, headers=superuser_token_headers)
    assert resp.status_code == 200


async def test_delete_user_me(client, async_session_test, superuser_token_headers):
    user, pswd = await create_random_user(db=async_session_test)
    token = await user_authentication_headers(
        client=client, email=user.email, password=pswd
    )
    url = await getURL("/user/me")
    resp = await client.delete(url, headers=token)
    assert resp.status_code == 200


async def test_update_user(client, async_session_test, superuser_token_headers):
    user, pswd = await create_random_user(db=async_session_test)

    url = await getURL(f"/user/{user.id}")
    user_upd = IUserUpdate(name="Papa", surname="Sviridov12")

    data = {"name": user_upd.name, "surname": user_upd.surname}
    resp = await client.patch(url, json=data, headers=superuser_token_headers)
    data_resp = resp.json()
    assert resp.status_code == 200
    data_resp = data_resp["data"]
    assert user_upd.name == data_resp["name"]
    assert user_upd.surname == data_resp["surname"]


async def update_password_me(client, async_session_test):
    user, pswd = await create_random_user(db=async_session_test)
    token = await user_authentication_headers(
        client=client, email=user.email, password=pswd
    )
    url = await getURL("/user/me/password")

    new_pasw = random_lower_string()
    body = IUserUpdatePassword()
    body.current_password = pswd
    body.new_password = new_pasw

    resp = await client.put(url, json=body, headers=token)
    assert resp.status_code == 200


async def test_update_user_me(client, async_session_test):
    user, pswd = await create_random_user(db=async_session_test)
    token = await user_authentication_headers(
        client=client, email=user.email, password=pswd
    )
    url = await getURL("/user/me")
    user_upd = IUserUpdateMe(name="Papa", surname="Sviridov")
    resp = await client.put(url, json=user_upd.model_dump(), headers=token)
    assert resp.status_code == 200
    data_resp = resp.json()
    data_resp = data_resp["data"]
    assert user_upd.name == data_resp["name"]
    assert user_upd.surname == data_resp["surname"]
