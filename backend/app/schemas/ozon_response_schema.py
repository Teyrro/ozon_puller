from typing import Any

from pydantic import AnyUrl, AwareDatetime, BaseModel, NaiveDatetime, PastDatetime


class Report(BaseModel):
    code: str
    status: str
    error: str
    file: AnyUrl | bytes | None
    report_type: str
    params: dict[str, Any]
    created_at: AwareDatetime | PastDatetime | NaiveDatetime


class OzonReportListResp(BaseModel):
    reports: list[Report]
    total: int


class Dimensions(BaseModel):
    id: str
    name: str


class Data(BaseModel):
    dimensions: list[Dimensions]
    metrics: list[float]


class MetricsData(BaseModel):
    data: list[Data]
    totals: list[float]


class OzonGetMetrixResp(BaseModel):
    result: MetricsData
    timestamp: AwareDatetime | PastDatetime | NaiveDatetime
