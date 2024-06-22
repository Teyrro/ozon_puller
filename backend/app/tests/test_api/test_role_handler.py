from app.schemas.role_schema import IRoleCreate, IRoleUpdate
from app.tests.utils.user import create_random_user, user_authentication_headers
from app.utils.getURL import getURL


async def test_get_roles(client, async_session_test, superuser_token_headers):
    url = await getURL("/role")
    resp = await client.get(url, headers=superuser_token_headers)

    assert resp.status_code == 200


async def test_get_role_by_id(client, async_session_test, superuser_token_headers):
    user, pswd = await create_random_user(db=async_session_test)
    token = await user_authentication_headers(
        client=client, email=user.email, password=pswd
    )
    url = await getURL(f"/role/{user.role_id}")
    resp = await client.get(url, headers=token)
    assert resp.status_code == 200


async def test_create_role(client, async_session_test, superuser_token_headers):
    url = await getURL("/role")
    role = IRoleCreate(name="Mama mia", description="Mama mia")
    role = IRoleCreate(name="Ma mia", description="Ma mia")

    resp = await client.post(
        url, json=role.model_dump(), headers=superuser_token_headers
    )
    assert resp.status_code == 201


async def test_update_role(client, async_session_test, superuser_token_headers):
    user, pswd = await create_random_user(db=async_session_test)
    url = await getURL(f"/role/{user.role_id}")
    role = IRoleUpdate()
    role.description = "Mama mia"
    resp = await client.put(
        url, json=role.model_dump(), headers=superuser_token_headers
    )
    assert resp.status_code == 200
