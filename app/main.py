from fastapi import FastAPI

from app.api.v1.api import api_router
from app.exceptions.common import AppException
from app.exceptions.handlers import app_exception_handler


app = FastAPI(
    title="Blog API",
    version="1.0.0",
)


app.add_exception_handler(
    AppException,
    app_exception_handler,
)


app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "Blog API is running",
    }