from io import BytesIO
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Params
from starlette import status
from starlette.responses import StreamingResponse

from app import crud
from app.api.deps import get_current_user
from app.schemas.ozon_report_schema import IOzonReportRead
from app.schemas.ozon_requests_schema import ReportType
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponsePaginated,
    create_response,
)
from app.schemas.role_schema import IRoleEnum

report_router = APIRouter()


@report_router.delete("/{report_id}", dependencies=[Depends(get_current_user())])
async def remove_report(report_id: UUID) -> IDeleteResponseBase[IOzonReportRead]:
    report = crud.ozon_report.get(id=report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report doesn't exist",
        )
    report = await crud.ozon_report.remove(id=report_id)
    return create_response(report, message="Report removed")


@report_router.post("/download/{report_id}", dependencies=[Depends(get_current_user())])
async def download_file(report_id: UUID) -> StreamingResponse:
    report = await crud.ozon_report.get(id=report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    filename = media_type = stream = None
    if report.report_type == ReportType.seller_products.lower():
        stream = BytesIO(report.report)
        media_type = "text/csv;charset=utf-8"
        filename = "users.csv"
    elif report.report_type == ReportType.seller_metrics.lower():
        stream = BytesIO(report.report)
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


@report_router.post(
    "/list",
    dependencies=[Depends(get_current_user([IRoleEnum.admin]))],
)
async def get_all_reports(
    params: Params = Depends(),
) -> IGetResponsePaginated[IOzonReportRead]:
    reports = await crud.ozon_report.get_multi_paginated(params=params)
    if not reports:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reports not found",
        )
    return create_response(reports, message="Reports retrieved")
