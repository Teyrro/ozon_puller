from celery import Celery

from app.core.config import settings

celery = Celery(
    "async_task",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    backend=str(settings.SYNC_CELERY_DATABASE_URI),
    include="app.api.celery_task",  # route where tasks are defined
)

beat_max_loop_interval = 10

beat_dburi = str(settings.SYNC_CELERY_BEAT_DATABASE_URI)

timezone = 'UTC'

worker_max_tasks_per_child = 10

config = {
    # 'beat_scheduler': beat_scheduler,  # The command line parameters are configured, so there is no need to write
    # them in the code here
    'beat_max_loop_interval': beat_max_loop_interval,
    'beat_dburi': beat_dburi,
    # 'beat_schema': 'celery',  # set this to none if you are using sqlite or you want all tables under default schema

    'timezone': timezone,
    'worker_max_tasks_per_child': worker_max_tasks_per_child
}

celery.conf.update(config)
celery.autodiscover_tasks()
