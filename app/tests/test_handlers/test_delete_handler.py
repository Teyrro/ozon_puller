from uuid import uuid4

from app.tests.conftest import create_test_auth_for_user


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": 0,
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data["user_id"] = await create_user_in_database(user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}",
                         headers=create_test_auth_for_user(user_data["email"]),
                         )
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    user_from_db = await get_user_from_database(user_data["user_id"])
    assert user_from_db.name == user_data["name"]
    assert user_from_db.surname == user_data["surname"]
    assert user_from_db.email == user_data["email"]
    assert user_from_db.is_active is False
    assert user_from_db.user_id == user_data["user_id"]


async def test_delete_user_not_found(client, create_user_in_database):
    user_data = {
        "user_id": 0,
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data["user_id"] = await create_user_in_database(user_data)
    user_id = uuid4()
    resp = client.delete(f"/user/?user_id={user_id}",
                         headers=create_test_auth_for_user(user_data["email"]))
    assert resp.status_code == 404
    assert resp.json() == {"detail": f"User with id {user_id} not found"}


async def test_delete_user_user_id_validation_error(client, create_user_in_database):
    user_data = {
        "user_id": 0,
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data["user_id"] = await create_user_in_database(user_data)
    resp = client.delete("/user/?user_id=123",
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


async def test_user_not_auth(client, create_user_in_database):
    user_data = {
        "user_id": 0,
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data["user_id"] = await create_user_in_database(user_data)
    user_id = uuid4()
    bad_auth_headers = create_test_auth_for_user(user_data["email"])
    bad_auth_headers["Authorization"] += "a"
    resp = client.delete(f"/user/?user_id={user_data['user_id']}",
                         headers=bad_auth_headers)
    assert resp.status_code == 401
    assert resp.json() == {'detail': 'Could not validate credentials'}


async def test_user_bad_cred(client, create_user_in_database):
    user_data = {
        "user_id": 0,
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",
    }
    user_data["user_id"] = await create_user_in_database(user_data)
    user_id = uuid4()
    resp = client.delete(f"/user/?user_id={user_id}",
                         headers=create_test_auth_for_user(user_data["email"] + "fwqef")
                         )
    assert resp.status_code == 401
    assert resp.json() == {'detail': 'Could not validate credentials'}


async def test_delete_user_no_jwt(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "password": "SampleHashedPass",

    }
    user_data["user_id"] = await create_user_in_database(user_data)
    user_id = uuid4()
    resp = client.delete(
        f"/user/?user_id={user_id}",
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}
