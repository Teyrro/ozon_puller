import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi_pagination import add_pagination
from sqlalchemy import AsyncAdaptedQueuePool, NullPool
from starlette.middleware.cors import CORSMiddleware

from app.api.main import main_api_router
from app.core.config import ModeEnum, settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(title="OzonPuller", generate_unique_id_function=custom_generate_unique_id)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=str(settings.ASYNC_DATABASE_URI),
    engine_args={
        "echo": False,
        "poolclass": NullPool
        if settings.MODE == ModeEnum.testing
        else AsyncAdaptedQueuePool
    },
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(main_api_router)
add_pagination(app)
if __name__ == "__main__":
    uvicorn.run(app, host=settings.DOMAIN, port=settings.PORT)
    # beat = celery.Beat(loglevel="debug")
    # beat.start_scheduler()
