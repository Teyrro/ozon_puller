import asyncio
import logging

from celery.schedules import crontab

from app.api.routes.servises.ozon_request import OzonRequestService
from app.core.celery import celery


@celery.task(
    ignore_result=True,
    name='task.download_reports'
)
def download_seller_reports():
    or_service: OzonRequestService = OzonRequestService()
    asyncio.get_event_loop().run_until_complete(or_service.download_reports())


@celery.task(
    ignore_result=True,
    name='task.generate_metrics'
)
def generate_metrics():
    or_service: OzonRequestService = OzonRequestService()
    asyncio.get_event_loop().run_until_complete(or_service.generate_metrics())


@celery.task(
    name='task.print_hello'
)
def print_hello():
    logging.info("Hello World!")


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(
        day_of_week="*/1",
        hour="2"),
        download_seller_reports.s(),
        name="every day at 2:00 AM, download product report"
    )
    sender.add_periodic_task(crontab(
        day_of_week="*/1",
        hour="2", minute="20"),
        generate_metrics.s(),
        name="every day at 2:20 AM, generate metrics"
    )
