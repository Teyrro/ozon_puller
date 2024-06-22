from app import crud
from app.tests.utils.user import (
    create_random_file,
    create_random_user,
    user_authentication_headers,
)
from app.utils.getURL import getURL


async def test_remove_report(client, async_session_test, superuser_token_headers):
    report = await create_random_file(db=async_session_test)
    report_in = await crud.ozon_report.get_last_by_report_type(
        type=report.report_type, db_session=async_session_test
    )
    url = await getURL(f"/report/{report_in.id}")
    user, pswd = await create_random_user(db=async_session_test)
    token = await user_authentication_headers(
        client=client, email=user.email, password=pswd
    )
    resp = await client.delete(url, headers=token)
    assert resp.status_code == 200


async def test_download_report(client, async_session_test, superuser_token_headers):
    report = await create_random_file(db=async_session_test)
    report_in = await crud.ozon_report.get_last_by_report_type(
        type=report.report_type, db_session=async_session_test
    )
    url = await getURL(f"/report/download/{report_in.id}")
    user, pswd = await create_random_user(db=async_session_test)
    token = await user_authentication_headers(
        client=client, email=user.email, password=pswd
    )
    resp = await client.post(url, headers=token)
    assert resp.status_code == 200


async def test_get_all_reports(client, async_session_test, superuser_token_headers):
    await create_random_file(db=async_session_test)
    await create_random_file(db=async_session_test)

    url = await getURL("/report/list")
    user, pswd = await create_random_user(db=async_session_test)
    token = await user_authentication_headers(
        client=client, email=user.email, password=pswd
    )
    resp = await client.post(url, headers=token)
    assert resp.status_code == 200
