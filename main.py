import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import main_api_router


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(title="OzonPuller", generate_unique_id_function=custom_generate_unique_id)

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
