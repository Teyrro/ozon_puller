import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.role_schema import IRoleEnum
from app.schemas.user_schema import IUserCreate
from app.tests.utils.user import create_random_user, get_role_id
from app.tests.utils.utils import random_email, random_lower_string


async def test_create_user(
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
    resp = await client.post(
        "/user/", content=user_in.model_dump_json(), headers=superuser_token_headers
    )
    data_from_resp = resp.json()
    data_from_resp = data_from_resp["data"]
    assert resp.status_code == 201
    assert data_from_resp["name"] == user_in.name
    assert data_from_resp["surname"] == user_in.surname
    assert data_from_resp["email"] == user_in.email
    assert data_from_resp["is_active"] is True


async def test_create_user_duplicate_email_error(
    client, async_session_test: AsyncSession, superuser_token_headers
):
    user = await create_random_user(db=async_session_test)
    user_in = IUserCreate(
        name="Michel",
        surname="Far",
        email=user.email,
        password=random_lower_string(),
        role_id=await get_role_id(role=IRoleEnum.user, db=async_session_test),
    )
    resp = await client.post(
        "/user/", content=user_in.model_dump_json(), headers=superuser_token_headers
    )
    assert resp.status_code == 503
    assert "Database error" in resp.json()["detail"]


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
    resp = await client.post(
        "/user/", json=user_data_for_creation, headers=superuser_token_headers
    )
    data_from_resp = resp.json()
    assert resp.status_code == expected_status_code
    assert data_from_resp == expected_detail
