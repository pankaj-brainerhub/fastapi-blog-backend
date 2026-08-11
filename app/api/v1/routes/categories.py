from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryListResponse,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=201,
)
def create_category(
    data: CategoryCreate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    return service.create(data)


@router.get(
    "",
    response_model=CategoryListResponse,
)
def list_categories(
    page: int = Query(
        default=1,
        ge=1,
    ),
    per_page: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    return service.list(
        page=page,
        per_page=per_page,
    )


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    return service.get(category_id)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    return service.update(
        category_id,
        data,
    )


@router.delete(
    "/{category_id}",
    status_code=204,
)
def delete_category(
    category_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    service.delete(category_id)