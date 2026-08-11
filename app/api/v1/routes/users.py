import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.response import ApiResponse, PaginatedData, PaginatedResponse
from app.schemas.user import (
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=PaginatedResponse[UserResponse],
)
def list_users(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    search: str | None = None,
    role_id: str | None = None,
    is_active: bool | None = None,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    result = service.list_users(
        page=page,
        per_page=per_page,
        search=search,
        role_id=role_id,
        is_active=is_active,
    )

    return PaginatedResponse(
        message="Users fetched successfully.",
        data=PaginatedData(
            items=result.items,
            total=result.total,
            page=result.page,
            per_page=result.per_page,
            total_pages=result.total_pages,
        ),
    )


@router.get(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
)
def get_user(
    user_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    user = service.get_user(user_id)

    return ApiResponse(
        message="User fetched successfully.",
        data=UserResponse.model_validate(user),
    )


@router.patch(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
)
def update_user(
    user_id: int,
    data: UserUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    user = service.update_user(user_id, data)

    return ApiResponse(
        message="User updated successfully.",
        data=UserResponse.model_validate(user),
    )


@router.delete(
    "/{user_id}",
    response_model=ApiResponse[None],
)
def delete_user(
    user_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    service.delete_user(user_id)

    return ApiResponse(
        message="User deactivated successfully.",
        data=None,
    )