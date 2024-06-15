import celery_typed_tasks
from celery import Celery

from app.core.config import settings

# def clean_tasks(task_names: list[str]):
#     session_manager = SessionManager()
#     session = session_manager.session_factory(str(settings.SYNC_CELERY_BEAT_DATABASE_URI))
#     for name in task_names:
#         with session_cleanup(session):
#             stmp = update(PeriodicTask).where(PeriodicTask.name == name).values(enabled=False)
#
#             session.execute(stmp)
#             session.commit()
#
#             PeriodicTaskChanged.update_from_session(session)


celery = Celery(
    "async_task",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    backend=str(settings.SYNC_CELERY_DATABASE_URI),
    include="app.api.celery_task",  # route where tasks are defined
    task_cls=celery_typed_tasks.TypedTask,
)

beat_max_loop_interval = 10

beat_dburi = str(settings.SYNC_CELERY_BEAT_DATABASE_URI)

timezone = "Asia/Novosibirsk"

worker_max_tasks_per_child = 3

config = {
    # 'beat_schedule': beat_schedule,
    # them in the code here
    "beat_max_loop_interval": beat_max_loop_interval,
    "beat_dburi": beat_dburi,
    # 'beat_schema': 'celery',  # set this to none if you are using sqlite, or you want all tables under default schema
    "timezone": timezone,
    "worker_max_tasks_per_child": worker_max_tasks_per_child,
}

celery.conf.update(config)
celery.autodiscover_tasks()
