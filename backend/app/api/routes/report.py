from io import BytesIO

from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from starlette.responses import StreamingResponse

from app import crud
from app.schemas.ozon_report_schema import IOzonReportRead
from app.schemas.ozon_requests_schema import ReportType
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponsePaginated,
    create_response,
)

report_router = APIRouter()


@report_router.delete("/")
async def remove_report(id) -> IDeleteResponseBase[IOzonReportRead]:
    report = await crud.ozon_report.remove(id=id)
    return create_response(report, message="Report removed")


@report_router.post("/download")
async def download_file(id) -> StreamingResponse:
    report = await crud.ozon_report.get(id=id)
    filename = media_type = stream = None
    if report.report_type == ReportType.seller_products.lower():
        stream = BytesIO(report.report)
        media_type = "text/csv;charset=utf-8"
        filename = "users.csv"
    elif report.report_type == ReportType.seller_metrics.lower():
        stream = BytesIO(report.report)
        media_type = "application/octet-stream"
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8"
        filename = "metrics.xlsx"
    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment;filename={filename}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
    return response


@report_router.post("/list")
async def get_all_reports(
    params: Params = Depends(),
) -> IGetResponsePaginated[IOzonReportRead]:
    reports = await crud.ozon_report.get_multi_paginated(params=params)
    return create_response(reports)
