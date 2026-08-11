from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.constants.post import PostStatus
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
        current_user=current_user,
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
    category_id: int | None = Query(
        default=None,
        gt=0,
    ),
    status: PostStatus | None = None,
    search: str | None = None,
    sort_by: str = Query(
        default="created_at",
    ),
    sort_order: str = Query(
        default="desc",
    ),
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    service = PostService(db)

    return service.list(
        page=page,
        per_page=per_page,
        current_user=current_user,
        category_id=category_id,
        status=status,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get(
    "/{post_id}",
    response_model=PostResponse,
)
def get_post(
    post_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    service = PostService(db)

    return service.get(
        post_id=post_id,
        current_user=current_user,
    )


@router.patch(
    "/{post_id}",
    response_model=PostResponse,
)
def update_post(
    post_id: int,
    data: PostUpdate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    service = PostService(db)

    return service.update(
        post_id=post_id,
        data=data,
        current_user=current_user,
    )


@router.delete(
    "/{post_id}",
    status_code=204,
)
def delete_post(
    post_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    service = PostService(db)

    service.delete(
        post_id=post_id,
        current_user=current_user,
    )