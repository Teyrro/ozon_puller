from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ReportType(str, Enum):
    all = "ALL",
    seller_products = "SELLER_PRODUCTS",
    seller_transactions = "SELLER_TRANSACTIONS",
    seller_product_prices = "SELLER_PRODUCT_PRICES",
    seller__stock = "SELLER_STOCK",
    seller_returns = "SELLER_RETURNS",
    seller_postings = "SELLER_POSTINGS",
    seller_finance = "SELLER_FINANCE",
    seller_product_discounted = "SELLER_PRODUCT_DISCOUNTED",
    seller_metrics = "SELLER_METRICS",


class OzonReportListReq(BaseModel):
    page: int
    page_size: int
    report_type: ReportType


class DimensionType(str, Enum):
    unknownDimension = "unknownDimension",
    sku = "sku"
    spu = "spu"
    day = "day"
    week = "week"
    month = "month"


class Metrics(str, Enum):
    revenue = "revenue"
    returns = "returns"
    ordered_units = "ordered_units"


class Order(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class SortedParams(BaseModel):
    order: Order
    key: Metrics


class OzonGetMetrixReq(BaseModel):
    date_from: datetime
    date_to: datetime
    metrics: list[Metrics]
    dimension: list[DimensionType]
    sort: list[SortedParams]
    limit: int
    offset: int
