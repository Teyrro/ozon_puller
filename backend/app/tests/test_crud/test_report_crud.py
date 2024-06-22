from datetime import datetime

from app import crud
from app.schemas.ozon_report_schema import IOzonReportCreate
from app.schemas.ozon_requests_schema import ReportType
from app.tests.utils.user import create_random_file


async def test_get_last_item_by_create_at(async_session_test):
    await create_random_file(db=async_session_test)
    report = await create_random_file(db=async_session_test)
    report_out = await crud.ozon_report.get_last_by_report_type(
        type=report.report_type, db_session=async_session_test
    )
    assert report_out == report
    assert report_out.report_type == report.report_type


async def test_create_seller_product(async_session_test):
    file = b"Hello World"
    orm_report = IOzonReportCreate(
        report=file,
        ozon_created_at=datetime.now(),
        report_type=ReportType.seller_products.lower(),
    )
    users = await crud.user.get_all_id(db_session=async_session_test)
    report = await crud.ozon_report.create_seller_report_for_all_users(
        users=users, db_session=async_session_test, report=orm_report
    )
    report_out = await crud.ozon_report.get(id=report.id, db_session=async_session_test)
    assert report_out.created_at == report.created_at


async def test_get_last_by_report_type(async_session_test):
    await create_random_file(db=async_session_test)
    report = await create_random_file(db=async_session_test)
    report_3 = await crud.ozon_report.get_last_by_report_type(
        type=ReportType.seller_products.lower(), db_session=async_session_test
    )

    assert report_3.created_at == report.created_at
