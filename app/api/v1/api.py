from fastapi import APIRouter

from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.categories import (
    router as categories_router,
)
from app.api.v1.routes.posts import router as posts_router
from app.api.v1.routes.users import router as users_router


api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(categories_router)
api_router.include_router(posts_router)