from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.post import (
    PostCreate,
    PostListResponse,
    PostResponse,
    PostUpdate,
)
from app.services.post_service import PostService


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post(
    "",
    response_model=PostResponse,
    status_code=201,
)
def create_post(
    data: PostCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    service = PostService(db)

    return service.create(
        data=data,
        user_id=current_user.id,
    )


@router.get(
    "",
    response_model=PostListResponse,
)
def list_posts(
    page: int = Query(
        default=1,
        ge=1,
    ),
    per_page: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    category_id: int | None = None,
    search: str | None = None,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    service = PostService(db)

    return service.list(
        page=page,
        per_page=per_page,
        category_id=category_id,
        search=search,
    )


@router.get(
    "/{post_id}",
    response_model=PostResponse,
)
def get_post(
    post_id: int,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PostService(db)

    return service.get(post_id)