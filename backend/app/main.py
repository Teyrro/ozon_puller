import sentry_sdk
from fastapi import FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi_pagination import add_pagination
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import AsyncAdaptedQueuePool, NullPool
from starlette.middleware.cors import CORSMiddleware

from app.api.main import main_api_router
from app.core.config import ModeEnum, settings

# def custom_generate_unique_id(route: APIRoute) -> str:
#     return f"{route.tags[0]}-{route.name}"


sentry_sdk.init(
    dsn="https://1390e288115dacca18dfb18c637adea9@o4507442072911872.ingest.de.sentry.io/4507442077368400",
)

app = FastAPI(
    title="OzonPuller",
    openapi_url=settings.API_V1_STR,
    # generate_unique_id_function=custom_generate_unique_id,
    debug=False,
)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=str(settings.ASYNC_DATABASE_URI),
    engine_args={
        "echo": True,
        "poolclass": NullPool
        if settings.MODE == ModeEnum.testing
        else AsyncAdaptedQueuePool,
    },
)

Instrumentator().instrument(app).expose(app)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"],
        # allow_headers=["*"],
        allow_headers=[
            "Accept",
            "Content-Type",
            "X-Requested-With",
            "Origin",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
    )

app.include_router(main_api_router, prefix=settings.API_V1_STR)
add_pagination(app)
