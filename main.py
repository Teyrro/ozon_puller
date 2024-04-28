import uvicorn
from fastapi import APIRouter, FastAPI

from app.api.routes.login import login_router
from app.api.routes.users import user_router

app = FastAPI(title="OzonPuller")


main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
