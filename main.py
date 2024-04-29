import uvicorn
from fastapi import FastAPI

from app.api.main import main_api_router

app = FastAPI(title="OzonPuller")

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
