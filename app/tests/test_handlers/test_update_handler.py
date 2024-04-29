import json
from uuid import uuid4

import pytest

from app.tests.conftest import create_test_auth_for_user


async def test_update_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": 0,
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data_updated = {
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "cheburek@kek.com",
    }
    user_data["user_id"] = await create_user_in_database(user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated),
        headers=create_test_auth_for_user(user_data["email"])
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    user_from_db = await get_user_from_database(user_data["user_id"])
    assert user_from_db.name == user_data_updated["name"]
    assert user_from_db.surname == user_data_updated["surname"]
    assert user_from_db.email == user_data_updated["email"]
    assert user_from_db.is_active is True
    assert user_from_db.user_id == user_data["user_id"]


async def test_update_user_check_one_is_updated(
    client, create_user_in_database, get_user_from_database
):
    user_data_1 = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data_2 = {
        "user_id": uuid4(),
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "ivan@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data_3 = {
        "user_id": uuid4(),
        "name": "Petr",
        "surname": "Petr",
        "email": "petr@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data_updated = {
        "name": "Nikifor",
        "surname": "Nikiforov",
        "email": "cheburek@kek.com",
    }
    for user_data in [user_data_1, user_data_2, user_data_3]:
        user_data["user_id"] = await create_user_in_database(user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}", data=json.dumps(user_data_updated),
        headers=create_test_auth_for_user(user_data["email"])
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data_1["user_id"])
    user_from_db = await get_user_from_database(user_data_1["user_id"])
    assert user_from_db.name == user_data_updated["name"]
    assert user_from_db.surname == user_data_updated["surname"]
    assert user_from_db.email == user_data_updated["email"]
    assert user_from_db.is_active is user_data_1["is_active"]
    assert user_from_db.user_id == user_data_1["user_id"]

    # check other users that data has not been changed
    user_from_db = await get_user_from_database(user_data_2["user_id"])
    assert user_from_db.name == user_data_2["name"]
    assert user_from_db.surname == user_data_2["surname"]
    assert user_from_db.email == user_data_2["email"]
    assert user_from_db.is_active is user_data_2["is_active"]
    assert user_from_db.user_id == user_data_2["user_id"]

    user_from_db = await get_user_from_database(user_data_3["user_id"])
    assert user_from_db.name == user_data_3["name"]
    assert user_from_db.surname == user_data_3["surname"]
    assert user_from_db.email == user_data_3["email"]
    assert user_from_db.is_active is user_data_3["is_active"]
    assert user_from_db.user_id == user_data_3["user_id"]


@pytest.mark.parametrize(
    "user_data_updated, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": "At least one parameter for user update info should be provided"
            },
        ),
        ({"name": "123"}, 422, {"detail": "Name should contains only letters"}),
        (
            {"email": ""},
            422,
            {
                "detail": [
                    {
                        "ctx": {
                            "reason": "The email address is not valid. It must have "
                            "exactly one @-sign."
                        },
                        "input": "",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: The email address is "
                        "not valid. It must have exactly one @-sign.",
                        "type": "value_error",
                    }
                ]
            },
        ),
        (
            {"surname": ""},
            422,
            {
                "detail": [
                    {
                        "ctx": {"min_length": 1},
                        "input": "",
                        "loc": ["body", "surname"],
                        "msg": "String should have at least 1 character",
                        "type": "string_too_short",
                    }
                ]
            },
        ),
        (
            {"name": ""},
            422,
            {
                "detail": [
                    {
                        "ctx": {"min_length": 1},
                        "input": "",
                        "loc": ["body", "name"],
                        "msg": "String should have at least 1 character",
                        "type": "string_too_short",
                    }
                ]
            },
        ),
        ({"surname": "123"}, 422, {"detail": "Surname should contains only letters"}),
        (
            {"email": "123"},
            422,
            {
                "detail": [
                    {
                        "ctx": {
                            "reason": "The email address is not valid. It must have "
                            "exactly one @-sign."
                        },
                        "input": "123",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: The email address is "
                        "not valid. It must have exactly one @-sign.",
                        "type": "value_error",
                    }
                ]
            },
        ),
    ],
)
async def test_update_user_validation_error(
    client,
    create_user_in_database,
    get_user_from_database,
    user_data_updated,
    expected_status_code,
    expected_detail,
):
    user_data = {
        "user_id": 0,
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data["user_id"] = await create_user_in_database(user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated),
        headers=create_test_auth_for_user(user_data["email"]))
    assert resp.status_code == expected_status_code
    resp_data = resp.json()
    assert resp_data == expected_detail


async def test_update_user_id_validation_error(client, create_user_in_database):
    user_data = {
        "user_id": 0,
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data_updated = {
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "cheburek@kek.com",
    }
    await create_user_in_database(user_data)
    resp = client.patch("/user/?user_id=123", data=json.dumps(user_data_updated),
                        headers=create_test_auth_for_user(user_data["email"]))
    assert resp.status_code == 422
    data_from_response = resp.json()
    assert data_from_response == {
        "detail": [
            {
                "ctx": {
                    "error": "invalid length: expected length 32 for simple "
                    "format, found 3"
                },
                "input": "123",
                "loc": ["query", "user_id"],
                "msg": "Input should be a valid UUID, invalid length: expected "
                "length 32 for simple format, found 3",
                "type": "uuid_parsing",
            }
        ]
    }


async def test_update_user_not_found_error(client, create_user_in_database):
    user_data = {
        "user_id": 0,
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data_updated = {
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "cheburek@kek.com",
    }
    await create_user_in_database(user_data)
    user_id = uuid4()
    resp = client.patch(f"/user/?user_id={user_id}", data=json.dumps(user_data_updated),
                        headers=create_test_auth_for_user(user_data["email"])
                        )
    assert resp.status_code == 404
    resp_data = resp.json()
    assert resp_data == {"detail": f"User with id {user_id} not found."}


async def test_update_user_duplicate_email_error(client, create_user_in_database):
    user_data_1 = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data_2 = {
        "user_id": uuid4(),
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "ivan@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data_updated = {
        "email": user_data_2["email"],
    }
    for user_data in [user_data_1, user_data_2]:
        user_data["user_id"] = await create_user_in_database(user_data)

    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_for_user(user_data_1["email"])
    )
    assert resp.status_code == 503
    assert (
        'duplicate key value violates unique constraint "users_email_key"'
        in resp.json()["detail"]
    )