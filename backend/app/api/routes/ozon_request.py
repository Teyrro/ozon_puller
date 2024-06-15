from fastapi import APIRouter

from app.api.celery_task import download_seller_reports, generate_metrics

ozon_request_router = APIRouter()


@ozon_request_router.post("/seller-products")
async def get_products():
    """
    Download .xlsx files from ozon API, one-time upload not exceeding 20 files

    """
    download_seller_reports.delay()
    # or_service: OzonRequestService = OzonRequestService()
    # await or_service.download_reports()


@ozon_request_router.post("/metrix")
async def get_metrix():
    """
    Generate .xlsx f    ile with metrix
    """
    generate_metrics.delay()
    # or_service: OzonRequestService = OzonRequestService()
    # await or_service.generate_metrics(delta=timedelta(days=14))
