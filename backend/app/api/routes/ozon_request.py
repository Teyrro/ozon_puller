from datetime import timedelta

from fastapi import APIRouter

from app.api.celery_task import generate_metrics, download_seller_reports
from app.api.routes.servises.ozon_request import OzonRequestService

ozon_request_router = APIRouter()


@ozon_request_router.post("/seller-products")
async def get_products():
    """
    Download .xlsx files from ozon API, one-time upload not exceeding 20 files

    """
    download_seller_reports.delay()


@ozon_request_router.post("/metrix")
async def get_metrix():
    """
    Generate .xlsx file with metrix
    """
    generate_metrics.delay()
    # or_service: OzonRequestService = OzonRequestService()
    # await or_service.generate_metrics(delta=timedelta(days=14))
