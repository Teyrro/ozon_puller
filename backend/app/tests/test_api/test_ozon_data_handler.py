from app.schemas.ozon_data_schema import IOzonDataCreate
from app.tests.utils.user import (
    create_random_ozon_data,
    create_random_user,
    user_authentication_headers,
)
from app.tests.utils.utils import random_lower_string
from app.utils.getURL import getURL


async def test_remove_ozon_data(client, async_session_test, superuser_token_headers):
    ozon_in, user_in, pswd = await create_random_ozon_data(db=async_session_test)
    url = await getURL(f"/ozon_data/{ozon_in.id}")
    token = await user_authentication_headers(
        client=client, email=user_in.email, password=pswd
    )
    resp = await client.delete(url, headers=token)
    assert resp.status_code == 200


async def test_create_ozon_data(client, async_session_test, superuser_token_headers):
    user_in, pswd = await create_random_user(db=async_session_test)
    token = await user_authentication_headers(
        client=client, email=user_in.email, password=pswd
    )
    client_id = random_lower_string()
    api_key = random_lower_string()
    ozon_in = IOzonDataCreate(
        api_key=api_key,
        client_id=client_id,
    )
    url = await getURL("/ozon_data/")
    resp = await client.post(url, json=ozon_in.model_dump(), headers=token)
    assert resp.status_code == 200


async def test_update_ozon_data_me(client, async_session_test, superuser_token_headers):
    ozon, user_in, pswd = await create_random_ozon_data(db=async_session_test)
    token = await user_authentication_headers(
        client=client, email=user_in.email, password=pswd
    )
    api_key = "random_lower_string()"
    ozon_in = {"api_key": api_key}
    url = await getURL("/ozon_data/me")
    resp = await client.patch(url, json=ozon_in, headers=token)
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"]["api_key"] == ozon_in["api_key"]


async def test_read_ozon_data(client, async_session_test, superuser_token_headers):
    ozon, user_in, pswd = await create_random_ozon_data(db=async_session_test)
    token = await user_authentication_headers(
        client=client, email=user_in.email, password=pswd
    )

    url = await getURL("/ozon_data/me")
    resp = await client.get(url, headers=token)
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"]["api_key"] == ozon.api_key
