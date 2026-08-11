from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.schemas.response import ApiResponse, PaginatedData, PaginatedResponse
from app.services.category_service import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "",
    response_model=ApiResponse[CategoryResponse],
    status_code=201,
)
def create_category(
    data: CategoryCreate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)
    category = service.create(data)

    return ApiResponse(
        message="Category created successfully.",
        data=CategoryResponse.model_validate(category),
    )


@router.get(
    "",
    response_model=PaginatedResponse[CategoryResponse],
)
def list_categories(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)
    result = service.list(page=page, per_page=per_page)

    return PaginatedResponse(
        message="Categories fetched successfully.",
        data=PaginatedData(
            items=result.items,
            total=result.total,
            page=result.page,
            per_page=result.per_page,
            total_pages=result.total_pages,
        ),
    )


@router.get(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
)
def get_category(
    category_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)
    category = service.get(category_id)

    return ApiResponse(
        message="Category fetched successfully.",
        data=CategoryResponse.model_validate(category),
    )


@router.patch(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)
    category = service.update(category_id, data)

    return ApiResponse(
        message="Category updated successfully.",
        data=CategoryResponse.model_validate(category),
    )


@router.delete(
    "/{category_id}",
    response_model=ApiResponse[None],
)
def delete_category(
    category_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)
    service.delete(category_id)

    return ApiResponse(
        message="Category deleted successfully.",
        data=None,
    )