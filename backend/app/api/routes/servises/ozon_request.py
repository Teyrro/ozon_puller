import asyncio
import io
import logging
from asyncio import Semaphore
from datetime import datetime, timedelta
from io import BytesIO
from time import sleep

import aiohttp
import polars as pl
import xlsxwriter
from fastapi import HTTPException
from polars import DataFrame
from starlette import status
from xlsxwriter.utility import xl_col_to_name
from xlsxwriter.worksheet import Worksheet

from app import crud
from app.api.deps import get_db
from app.core.config import settings
from app.crud.ozon_data_crud import CRUDOzonData
from app.crud.ozon_report_crud import CRUDOzonReport
from app.crud.user_crud import CRUDUser
from app.models import OzonReport
from app.schemas.ozon_report_schema import IOzonReportCreate, IOzonReportUpdate
from app.schemas.ozon_requests_schema import (
    DimensionType,
    Metrics,
    Order,
    OzonGetMetrixReq,
    OzonReportListReq,
    ReportType,
    SortedParams,
)
from app.schemas.ozon_response_schema import (
    OzonGetMetrixResp,
    OzonReportListResp,
    Report,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OzonRequestService:
    headers = {
        "Host": settings.OZON_HOST,
        "Client-Id": "",
        "Api-Key": "",
        "Content-Type": "application/json",
    }

    sheets = ["Handbook", "Metrics", "OrdersHistory", "Stock"]

    CHUNK_SIZE = 50 * 1024

    def __init__(self):
        self.or_crud: CRUDOzonReport = crud.ozon_report
        self.od_crud: CRUDOzonData = crud.ozon_data
        self.u_crud: CRUDUser = crud.user

    async def _update_headers(self, user_id):
        """
        Set api-key and client_id in headers by user_id
        """
        async with get_db() as session:
            ozon_data = await self.od_crud.get_by_user_id(
                id=user_id, db_session=session
            )
        self.headers["Client-Id"] = ozon_data.client_id
        self.headers["Api-Key"] = ozon_data.api_key

    async def _get_reports(self, user_id):
        await self._update_headers(user_id)
        page = 1
        while True:
            body = OzonReportListReq(
                page=page, page_size=1000, report_type=ReportType.all
            )
            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    settings.OZON_URL + "/v1/report/list",
                    headers=self.headers,
                    data=body.json(),
                )
                data = await response.json()
                data = data["result"]
                data = OzonReportListResp.model_validate(data)
                yield (report for report in data.reports)
                if data.total - body.page * body.page_size > 0:
                    page += 1
                else:
                    break

    @staticmethod
    async def _download_file(url: str, req_sema: Semaphore):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if 200 <= response.status <= 300:
                    async with req_sema:
                        return await response.read()

    async def _download_report(
        self, report: Report, last_date_report_in_db: OzonReport, req_sema: Semaphore
    ):
        if (
            last_date_report_in_db
            and report.created_at <= last_date_report_in_db.ozon_created_at
            or report.file == ""
            or report.status != "success"
        ):
            return None
        report.file = await self._download_file(str(report.file), req_sema)
        return report

    async def download_reports(self):
        async with get_db() as session:
            last_report_date = await self.or_crud.get_last_item_by_created_at(
                db_session=session
            )
            users = await self.u_crud.get_all_id(db_session=session)

            # need for get ozon api-key, it's and system, and user
            admin_id = await self.u_crud.get_admin_id(db_session=session)
            req_sema = asyncio.Semaphore(value=20)
            async for reports in self._get_reports(admin_id):
                download_futures = [
                    self._download_report(report, last_report_date, req_sema)
                    for report in reports
                ]
                for future in asyncio.as_completed(download_futures):
                    report = await future
                    if (report and report.file) is not None:
                        orm_report = IOzonReportCreate(
                            report=report.file,
                            ozon_created_at=report.created_at,
                            report_type=report.report_type,
                        )
                        await self.or_crud.create_seller_report_for_all_users(
                            users=users,
                            report=orm_report,
                            db_session=session,
                        )
                        req_sema.release()

    @staticmethod
    async def _fill_init_data_stock(df: DataFrame):
        col_names = [
            "№",
            "Заказано за 14 дней",
            "Среднесуточный объем заказов, шт",
            "Прогноз оборачиваемости FBO, дн",
            "Возвраты за 14 дн",
            "Динамика заказов",
        ]
        stock: DataFrame = df.select(pl.selectors.by_index(0, 17, 20))
        stock = stock.select(
            pl.lit(pl.arange(1, stock.shape[0] + 1, eager=True)).alias(col_names[0]),
            pl.all(),
        )
        for col in col_names[1:]:
            stock = stock.with_columns(pl.lit(None).alias(col))

        return stock

    async def _generate_metrics(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        delta: timedelta | None = None,
    ):
        async with get_db() as session:
            admin_id = await self.u_crud.get_admin_id(db_session=session)
        await self._update_headers(admin_id)

        if date_to is None:
            date_to = datetime.now()
        elif date_to > datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data to cannot be more than today's date",
            )
        if date_from is None:
            if delta is None:
                delta = timedelta(days=14)
            date_from = date_to - delta
        offset = 0
        limit = 1000
        col_names = {
            "sku": pl.Null,
            "product_id": pl.Int64,
            "ordered": pl.Float64,
            "returns": pl.Float64,
        }
        df = pl.DataFrame(schema=col_names)
        while True:
            body = OzonGetMetrixReq(
                date_from=date_from,
                date_to=date_to,
                metrics=[Metrics.ordered_units, Metrics.returns],
                dimension=[DimensionType.sku],
                sort=[SortedParams(key=Metrics.ordered_units, order=Order.DESC)],
                limit=limit,
                offset=offset,
            )
            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    settings.OZON_URL + "/v1/analytics/data",
                    headers=self.headers,
                    data=body.json(),
                )
                if (
                    status.HTTP_200_OK
                    <= response.status
                    <= status.HTTP_300_MULTIPLE_CHOICES
                ):
                    result = await response.json()
                    metrics = OzonGetMetrixResp.model_validate(result).result
                elif response.status == status.HTTP_429_TOO_MANY_REQUESTS:
                    logger.info("Too many requests, start waiting process on 61 second")
                    delay_for_next_request = 61
                    sleep(delay_for_next_request)
                else:
                    logger.info(offset)
                    raise Exception(response.status)
                if metrics and metrics.data:
                    offset += limit
                else:
                    break
            output_data = []
            for data in metrics.data:
                product_id = int(data.dimensions[0].id)
                order = data.metrics[0]
                returns = data.metrics[1]
                output_data.append((None, product_id, order, returns))
            temp_df = pl.DataFrame(data=output_data, schema=col_names)
            df = df.vstack(temp_df)

        return df

    async def _generate_templates(self):
        async with get_db() as session:
            report = await self.or_crud.get_last_item_by_created_at(db_session=session)
        df = pl.read_csv(BytesIO(report.report), separator=";")
        handbook: DataFrame = df.select(pl.selectors.by_index(0, 2, 3, 5))
        history_order = df.select(pl.selectors.by_index(0))
        stock = await self._fill_init_data_stock(df)

        names_sheets = list(
            zip(
                self.sheets[:1] + self.sheets[2:],
                [handbook, history_order, stock],
                strict=False,
            )
        )
        await self.save_dataframes(names_sheets)

    @staticmethod
    async def get_sku_14_days_and_avg_columns(
        metrics_sheet, spark_cols, sku_series, sheet_to
    ) -> DataFrame:
        sku_avg = (
            metrics_sheet.select(*spark_cols)
            .with_columns(
                pl.mean_horizontal(pl.all()).alias("avg"),
            )
            .with_columns(
                sku_series.alias("sku"),
            )
            .select("sku", "avg")
            .group_by("sku")
            .agg(pl.col("avg").sum())
        )
        stock_name, stock_sheet = sheet_to
        sku_14_days = (
            stock_sheet.select(pl.nth([1, 4]))
            .group_by(stock_sheet.columns[1])
            .agg(pl.col(stock_sheet.columns[4]).sum())
        )
        sku_14_days_avg = (
            sku_14_days.join(
                other=sku_avg,
                left_on=sku_14_days.columns[0],
                right_on="sku",
                how="inner",
            )
            .fill_null(0)
            .fill_nan(0)
        )
        return sku_14_days_avg.sort(sku_14_days_avg.columns[0])

    async def add_sparklines(
        self,
        sheet_writer: Worksheet,
        sheet_from: tuple[str, DataFrame],
        sheet_to: tuple[str, DataFrame],
    ):
        metrix_name, metrics_sheet = sheet_from
        length = len(metrics_sheet.columns)
        last_letter = xl_col_to_name(length - 1)
        if length > 5:
            spark_cols = metrics_sheet.columns[-6:-1]
        else:
            spark_cols = metrics_sheet.columns[1:-1]
        sku_series = metrics_sheet.select(pl.selectors.by_index(0)).to_series()
        sku_14_days_avg = await self.get_sku_14_days_and_avg_columns(
            metrics_sheet, spark_cols, sku_series, sheet_to
        )
        rows, cols = sheet_to[1].shape
        for ind_row, orders_14_d_and_avg in enumerate(sku_14_days_avg.rows(), 1):
            if orders_14_d_and_avg[1] > orders_14_d_and_avg[2]:
                color = "#008000"
            elif orders_14_d_and_avg[1] == orders_14_d_and_avg[2]:
                color = "#808080"
            else:
                color = "#FF0000"

            sheet_writer.add_sparkline(
                ind_row,
                cols - 1,
                {
                    "range": f"'{sheet_from[0]}'!B{ind_row + 1}:{last_letter}{ind_row + 1}",
                    "series_color": color,
                },
            )

    async def save_to_excel(
        self, nms_sh: list[tuple[str, DataFrame]], add_sparks: bool = False
    ) -> BytesIO:
        file = io.BytesIO()
        wb = xlsxwriter.Workbook(file)
        for name, sheet in nms_sh:
            if add_sparks and name == self.sheets[3]:
                sheet_from = nms_sh[2]
                sheet_writer = wb.add_worksheet(name)
                await self.add_sparklines(sheet_writer, sheet_from, (name, sheet))

            sheet.write_excel(wb, worksheet=name, autofit=True, autofilter=True)
        wb.close()
        return file

    async def save_dataframes(
        self,
        nms_dfs: list[tuple[str, DataFrame]],
        is_update: bool = False,
        add_sparks: bool = False,
    ):
        file = await self.save_to_excel(nms_dfs, add_sparks)
        async with get_db() as session:
            users = await self.u_crud.get_all_id(db_session=session)

            if is_update:
                orm_report = IOzonReportUpdate(
                    report=file.getvalue(),
                    ozon_created_at=None,
                    report_type=ReportType.seller_metrics.lower(),
                )
                report = await self.or_crud.get_last_by_report_type(
                    type=ReportType.seller_metrics.lower(), db_session=session
                )
                await self.or_crud.update(
                    obj_current=report,
                    obj_new=orm_report,
                    db_session=session,
                )
            else:
                orm_report = IOzonReportCreate(
                    report=file.getvalue(),
                    ozon_created_at=None,
                    report_type=ReportType.seller_metrics.lower(),
                )
                await self.or_crud.create_seller_report_for_all_users(
                    users=users, report=orm_report, db_session=session
                )

    @staticmethod
    async def fill_stock(stock: DataFrame, metrics: DataFrame, delta: timedelta):
        for ind_metr, ind_st in [(2, 4), (3, 7)]:
            sku_stock = stock.columns[1]
            sku_metrics = metrics.columns[0]
            metrics_curr_col_name = metrics.columns[ind_metr]
            stock_curr_col_name = stock.columns[ind_st]

            stock: DataFrame = (
                stock.join(
                    metrics.select(pl.nth([0, ind_metr])),
                    left_on=sku_stock,
                    right_on=sku_metrics,
                    how="left",
                )
                .with_columns(
                    pl.col(stock_curr_col_name).fill_null(pl.col(metrics_curr_col_name))
                )
                .drop(metrics_curr_col_name)
            )
        stock = stock.with_columns(
            pl.col(stock.columns[5]).fill_null(pl.col(stock.columns[4]) / delta.days),
        )
        stock = stock.with_columns(
            (pl.col(stock.columns[2]) / pl.col(stock.columns[5])).alias(
                stock.columns[6]
            )
        )

        stock = stock.fill_nan(0).fill_null(0)
        stock = stock.with_columns(
            pl.when(pl.col(pl.Float64).is_infinite())
            .then(0)
            .otherwise(pl.col(pl.Float64))
            .keep_name()
        )
        stock.group_by(stock.columns[1])
        return stock

    async def pull_reports_from_db(self, delta: timedelta = None):
        if delta is None:
            delta = timedelta(14)
        async with get_db() as session:
            o_report = await self.or_crud.get_last_item_by_created_at(
                db_session=session
            )
        if o_report is None:
            return delta, -1, None
        async with get_db() as session:
            report = await self.or_crud.get_last_by_report_type(
                type=ReportType.seller_metrics.lower(), db_session=session
            )
        return delta, o_report, report

    @staticmethod
    async def prepare_metrics(metrics, hb):
        sku_col = metrics.columns[0]
        sku_product_id_col = hb.select(pl.nth([0, 1]))

        metrics = (
            metrics.join(
                left_on=metrics.columns[1],
                right_on=sku_product_id_col.columns[1],
                how="inner",
                other=sku_product_id_col,
            )
        ).drop(sku_col)
        metrics = metrics.select(pl.nth([3, 0, 1, 2]))

        return metrics.group_by(metrics.columns[0]).agg(pl.selectors.numeric().sum())

    async def _fill_data_metrics(self, date_from, date_to, delta: timedelta = None):
        delta, o_report, report = await self.pull_reports_from_db(delta)
        if o_report == -1:
            return
        df = pl.read_csv(BytesIO(o_report.report), separator=";")
        stock = await self._fill_init_data_stock(df)

        hb = pl.read_excel(BytesIO(report.report), sheet_name="Handbook")
        ho = pl.read_excel(BytesIO(report.report), sheet_name="OrdersHistory")
        metrics = await self._generate_metrics(
            date_from=date_from, date_to=date_to, delta=delta
        )

        metrics = await self.prepare_metrics(metrics, hb)

        stock = await self.fill_stock(stock, metrics, delta)

        delta_by_days = (
            stock.select(pl.selectors.by_index(1, 4))
            .clone()
            .with_columns((pl.col(stock.columns[4])).alias(str(datetime.today())))
            .drop(stock.columns[4])
        )
        ho = (
            ho.join(
                delta_by_days,
                left_on=ho.columns[0],
                right_on=delta_by_days.columns[0],
                how="left",
            )
            .fill_null(0)
            .fill_nan(0)
            .group_by(ho.columns[0])
            .agg(pl.selectors.numeric().sum())
        )

        stock.sort(stock.columns[1])
        metrics.sort(metrics.columns[0])
        ho.sort(ho.columns[0])
        # for sparks need more than current metrics info
        add_sparks = len(ho.columns) > 2
        names_dfs = list(zip(self.sheets, [hb, metrics, ho, stock], strict=False))

        await self.save_dataframes(names_dfs, False, add_sparks)

    async def generate_metrics(
        self,
        date_from: datetime = None,
        date_to: datetime = None,
        delta: timedelta | None = None,
    ):
        async with get_db() as session:
            report = await self.or_crud.get_last_by_report_type(
                type=ReportType.seller_metrics.lower(), db_session=session
            )
            if report is None:
                await self._generate_templates()
        await self._fill_data_metrics(date_from, date_to, delta)
